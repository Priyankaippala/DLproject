"use client"

export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-between p-24">
     <div className="container">
      <h1>Face Recognition Web App</h1>
      <img id="videoElement" src="/api/upload_file" alt="Video Feed" />
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
