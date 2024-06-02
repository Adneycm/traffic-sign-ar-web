import React, { useState } from 'react';
import './VideoInput.css';

const VideoInput = () => {
  const [videoSrc, setVideoSrc] = useState(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('video/')) {
      const url = URL.createObjectURL(file);
      setVideoSrc(url);
      await uploadFile(file); ////////////
    }
  };

  const handleDrop = async (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('video/')) {
      const url = URL.createObjectURL(file);
      setVideoSrc(url);
      await uploadFile(file); ////////////
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('video', file);

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload video');
      }

      const data = await response.json();
      console.log(data); // Handle response from the backend
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <div
        className="video-upload-placeholder"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => document.getElementById('video-upload-input').click()}
      >
        <p>Drag and drop your video here, or click to upload</p>
        <input
          id="video-upload-input"
          type="file"
          accept="video/*"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </div>
      {videoSrc && (
        <video controls src={videoSrc} className="video-display" />
      )}
    </div>
  );
};

export default VideoInput;