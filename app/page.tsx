"use client";
import { useState } from "react";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [outputImage, setOutputImage] = useState<string | null>(null);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    if (event.target.files) {
      setSelectedFile(event.target.files[0]);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) return;
    const formData = new FormData();
    formData.append("img", selectedFile);

    try {
      const response = await fetch("/", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      setOutputImage(data.outputImage);
    } catch (error) {
      console.error("Error uploading file:", error);
    }
  };

  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
      <div className="container">
        <h1>Face Recognition Web App</h1>
        <input type="file" onChange={handleFileChange} />
        <button onClick={handleUpload}>Upload</button>
        {outputImage && (
          <img src={`/static/output/${outputImage}`} alt="Processed Face" />
        )}
        <style jsx>{`
          body {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
          }
          .container {
            text-align: center;
          }
          img {
            border: 2px solid black;
          }
        `}</style>
      </div>
    </main>
  );
}
