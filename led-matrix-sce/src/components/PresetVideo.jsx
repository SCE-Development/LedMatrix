import React from 'react';
import '../styles/PresetVideo.css';

const PresetVideo = ({ presets }) => {
    // Array of 9 preset videos (you can modify this later with actual presets)
    // const presets = Array(9).fill(null);

    function addVideo(newVideo) {
        presets.unshift(newVideo);
        presets.pop();
    }

    return (
        <div className="preset-video-container">
            <h1 className="preset-video-title">Preset Videos</h1>
            <div className="preset-video-grid">
                {presets.map((_, index) => (
                    <div key={index} className="preset-video-item">
                        {<button>Preset {index + 1}</button>}
                    </div>
                ))}
            </div>
        </div>
    );
};

export default PresetVideo;
