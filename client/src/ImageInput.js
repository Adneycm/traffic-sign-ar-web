import React, { useState } from 'react';
import './ImageInput.css';

const ImageInput = () => {
  const [imageSrc, setImageSrc] = useState(null);
  const [processedImageSrc, setProcessedImageSrc] = useState(null);

  const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (file && file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      setImageSrc(url);
      await uploadFile(file);
    }
  };

  const handleDrop = async (event) => {
    event.preventDefault();
    const file = event.dataTransfer.files[0];
    if (file && file.type.startsWith('image/')) {
      const url = URL.createObjectURL(file);
      setImageSrc(url);
      await uploadFile(file);
    }
  };

  const handleDragOver = (event) => {
    event.preventDefault();
  };

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append('media', file);  // Ensure the formData key matches the backend

    try {
      const response = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Failed to upload image');
      }

      const data = await response.json();
      console.log(data); // Handle response from the backend

      if (data.modifiedMediaUrl) {
        setProcessedImageSrc(`http://localhost:5000${data.modifiedMediaUrl}`);
      }
    } catch (error) {
      console.error(error);
    }
  };

  return (
    <div>
      <div
        className="image-upload-placeholder"
        onDrop={handleDrop}
        onDragOver={handleDragOver}
        onClick={() => document.getElementById('image-upload-input').click()}
      >
        <p>Drag and drop your image here, or click to upload</p>
        <input
          id="image-upload-input"
          type="file"
          accept="image/*"
          style={{ display: 'none' }}
          onChange={handleFileChange}
        />
      </div>
      {imageSrc && (
        <div>
          <p>Original Image:</p>
          <img src={imageSrc} alt="Original" className="image-display" />
        </div>
      )}
      {processedImageSrc && (
        <div>
          <p>Processed Image:</p>
          <img src={processedImageSrc} alt="Processed" className="image-display" />
        </div>
      )}
    </div>
  );
};

export default ImageInput;