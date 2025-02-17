import FileUpload from "../components/FileUpload";
import Button from "../components/Buttons";
import '../styles/Announcement-Dashboard.css';
import PresetVideo from "../components/PresetVideo";
import PresetImage from "../components/PresetImage";

const AnnouncementDashboard = () => {
    const videoPresets = Array(9).fill(null);
    const imagePresets = Array(9).fill(null);
    // useEffect hook here, using FileUpload.handleImageUpload()
    
    return (
        <div className="announcement-container">
            <div className="image-upload-section">
                <FileUpload />
            </div>
            <div className="button-section">
                <Button />
            </div>
            <div className="preset-video-section">
                <PresetVideo presets={videoPresets}/>
            </div>
            <div className="preset-image-section">
                <PresetImage presets={imagePresets}/>
            </div>
        </div>
    );
};

export default AnnouncementDashboard;