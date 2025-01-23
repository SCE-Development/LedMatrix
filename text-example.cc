#include "led-matrix.h"
#include "graphics.h"
#include <curl/curl.h>
#include <nlohmann/json.hpp>
#include <signal.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <vector>
#include <string>

using namespace rgb_matrix;
using json = nlohmann::json;

// Global for interrupt handling:
static volatile bool interrupt_received = false;
static void InterruptHandler(int signo) {
  interrupt_received = true;
}

// Helper to fetch data from the API
static size_t WriteCallback(void* contents, size_t size, size_t nmemb, void* userp) {
  ((std::string*)userp)->append((char*)contents, size * nmemb);
  return size * nmemb;
}

std::string FetchLeaderboard(const std::string& url) {
  CURL* curl;
  CURLcode res;
  std::string readBuffer;

  curl = curl_easy_init();
  if (curl) {
    curl_easy_setopt(curl, CURLOPT_URL, url.c_str());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, WriteCallback);
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &readBuffer);
    res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
      fprintf(stderr, "curl_easy_perform() failed: %s\n", curl_easy_strerror(res));
    }
    curl_easy_cleanup(curl);
  }
  return readBuffer;
}

void DisplayLeaderboard(RGBMatrix* canvas, const rgb_matrix::Font& font, const std::string& leaderboard_data) {
  // Parse leaderboard JSON
  json leaderboard;
  try {
    leaderboard = json::parse(leaderboard_data);
  } catch (...) {
    fprintf(stderr, "Error parsing JSON data\n");
    return;
  }

  // Clear the canvas
  canvas->Clear();

  // Set text color
  Color text_color(255, 255, 255); // White text

  int x = 1;
  int y = 6;

  // Draw Title
  rgb_matrix::DrawText(canvas, font, x, y, text_color, NULL, "LeetCode", 0);
  y += font.height() + 2; // Move down for the next line
  rgb_matrix::DrawText(canvas, font, x, y, text_color, NULL, "Leaderboard", 0);
  y += font.height() + 2; // Move down for the leaderboard entries

  // Draw Leaderboard Entries
  int rank = 1;
  for (const auto& entry : leaderboard) {
    std::string username = entry["username"];
    char buffer[64];
    snprintf(buffer, sizeof(buffer), "%d. %s", rank, username.c_str());

    rgb_matrix::DrawText(canvas, font, x, y, text_color, NULL, buffer, 0);
    y += font.height() + 2;
    rank++;
    if (rank > 3) break; // Only display top 3
  }
}

int main(int argc, char *argv[]) {
  // --------------------------------------------------------------------------
  // 1. Parse LED matrix flags
  // --------------------------------------------------------------------------
  RGBMatrix::Options matrix_options;
  rgb_matrix::RuntimeOptions runtime_opt;
  if (!rgb_matrix::ParseOptionsFromFlags(&argc, &argv,
                                         &matrix_options, &runtime_opt)) {
    fprintf(stderr, "Couldn't parse options.\n");
    return 1;
  }

  // --------------------------------------------------------------------------
  // 2. Load font
  // --------------------------------------------------------------------------
  const char* bdf_font_file = "./5x7.bdf";
  rgb_matrix::Font font;
  if (!font.LoadFont(bdf_font_file)) {
    fprintf(stderr, "Couldn't load font '%s'\n", bdf_font_file);
    return 1;
  }

  // --------------------------------------------------------------------------
  // 3. Create the matrix & set up signal handling
  // --------------------------------------------------------------------------
  RGBMatrix* canvas = RGBMatrix::CreateFromOptions(matrix_options, runtime_opt);
  if (!canvas) {
    return 1;
  }

  signal(SIGINT, InterruptHandler);
  signal(SIGTERM, InterruptHandler);

  // --------------------------------------------------------------------------
  // 4. Loop to fetch and display the leaderboard every minute
  // --------------------------------------------------------------------------
  const std::string api_url = "http://0.0.0.0:8001/leaderboard";

  while (!interrupt_received) {
    std::string leaderboard_data = FetchLeaderboard(api_url);
    DisplayLeaderboard(canvas, font, leaderboard_data);

    // Wait for 60 seconds before refreshing
    for (int i = 0; i < 60 && !interrupt_received; ++i) {
      sleep(1);
    }
  }

  // --------------------------------------------------------------------------
  // 5. Cleanup
  // --------------------------------------------------------------------------
  canvas->Clear();
  delete canvas;

  return 0;
}
