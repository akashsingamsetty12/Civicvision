const imgTab = document.getElementById("imgTab");
const vidTab = document.getElementById("vidTab");
const liveTab = document.getElementById("liveTab");
const BACKEND_URL = "";

const imgSec = document.getElementById("image-section");
const vidSec = document.getElementById("video-section");
const liveSec = document.getElementById("live-section");

const imageResult = document.getElementById("imageResult");
const videoResult = document.getElementById("videoResult");
const liveCanvas = document.getElementById("liveResultCanvas");
const ctx = liveCanvas.getContext("2d");

function switchTab(sec){
  imgSec.style.display="none";
  vidSec.style.display="none";
  liveSec.style.display="none";
  sec.style.display="block";
  
  // Clear all results and reset counts
  imageResult.style.display="none";
  videoResult.style.display="none";
  liveCanvas.style.display="none";
  imageResult.src = "";
  videoResult.src="";
  
  // Reset counts to 0
  document.getElementById("potholeCount").innerText="0";
  document.getElementById("plasticCount").innerText="0";
  document.getElementById("litterCount").innerText="0";
  
  imgTab.classList.remove("active");
  vidTab.classList.remove("active");
  liveTab.classList.remove("active");
  
  if(sec===imgSec) imgTab.classList.add("active");
  else if(sec===vidSec) vidTab.classList.add("active");
  else if(sec===liveSec) liveTab.classList.add("active");
}

imgTab.onclick=()=>switchTab(imgSec);
vidTab.onclick=()=>switchTab(vidSec);
liveTab.onclick=()=>switchTab(liveSec);

function setCounts(c){
  potholeCount.innerText=c.pothole;
  plasticCount.innerText=c.plastic;
  litterCount.innerText=c.otherlitter;
}

/* IMAGE */
imageForm.onsubmit=async(e)=>{
  e.preventDefault();
  const fd=new FormData(imageForm);
  
  const progressContainer = document.getElementById("imageProgressContainer");
  const progressBar = document.getElementById("imageProgressBar");
  const progressPercent = document.getElementById("imageProgressPercent");
  const estimatedTime = document.getElementById("imageEstimatedTime");
  const detectBtn = imageForm.querySelector(".detect-btn");
  
  progressContainer.style.display = "block";
  detectBtn.disabled = true;
  detectBtn.innerText = "⏳ Processing...";
  
  const startTime = Date.now();
  let progress = 0;
  
  // Update progress based on elapsed time (assume 3 seconds typical for image)
  const updateInterval = setInterval(() => {
    const elapsed = (Date.now() - startTime) / 1000; // seconds
    progress = Math.min((elapsed / 3) * 100, 90); // Cap at 90% until done
    progressBar.style.width = progress + "%";
    progressPercent.innerText = Math.floor(progress) + "%";
    
    const remaining = Math.max(0, 3 - elapsed);
    estimatedTime.innerText = remaining > 0 ? `⏱️ ${remaining.toFixed(1)}s remaining` : "";
  }, 100);
  
  try {
    const res=await fetch(`${BACKEND_URL}/detect/image`,{method:"POST",body:fd});
    const data=await res.json();
    
    clearInterval(updateInterval);
    progressBar.style.width = "100%";
    progressPercent.innerText = "100%";
    estimatedTime.innerText = "✅ Complete!";
    
    imageResult.src = BACKEND_URL + data.image_url + "?t=" + Date.now();
    imageResult.style.display="block";
    videoResult.style.display="none";
    liveCanvas.style.display="none";
    setCounts(data.counts);
    
    setTimeout(() => {
      progressContainer.style.display = "none";
      progressBar.style.width = "0%";
      progressPercent.innerText = "0%";
      estimatedTime.innerText = "";
    }, 1500);
  } catch (error) {
    clearInterval(updateInterval);
    progressContainer.style.display = "none";
    console.error("Error:", error);
  } finally {
    detectBtn.disabled = false;
    detectBtn.innerText = "🔍 Detect Image";
  }
};

imageForm.file.onchange=(e)=>{
  imageFileName.innerText=e.target.files[0].name;
};

/* VIDEO */
videoForm.onsubmit=async(e)=>{
  e.preventDefault();
  const fd=new FormData(videoForm);
  
  const progressContainer = document.getElementById("videoProgressContainer");
  const progressBar = document.getElementById("videoProgressBar");
  const progressPercent = document.getElementById("videoProgressPercent");
  const progressText = document.getElementById("videoProgressText");
  const detectBtn = videoForm.querySelector(".detect-btn");
  
  // Show progress bar and disable button
  progressContainer.style.display = "block";
  progressText.innerText = "Processing...";
  detectBtn.disabled = true;
  detectBtn.innerText = "⏳ Processing...";
  
  // Simulate progress
  let progress = 0;
  const progressInterval = setInterval(() => {
    if (progress < 85) {
      progress += Math.random() * 25;
      if (progress > 85) progress = 85;
      progressBar.style.width = progress + "%";
      progressPercent.innerText = Math.floor(progress) + "%";
    }
  }, 500);
  
  try {
    console.log("📤 Sending video to backend...");
    const res=await fetch(`${BACKEND_URL}/detect/video`,{method:"POST",body:fd});
    const data=await res.json();
    
    console.log("📥 Video response received:", data);
    
    if (data.error) {
      console.error("❌ Error from backend:", data.error);
      alert("Error processing video: " + data.error);
      clearInterval(progressInterval);
      progressContainer.style.display = "none";
      throw new Error(data.error);
    }
    
    // Complete progress
    clearInterval(progressInterval);
    progressBar.style.width = "100%";
    progressPercent.innerText = "100%";
    progressText.innerText = "✅ Complete! Loading video...";
    
    // Wait longer to ensure file is fully written to disk
    await new Promise(resolve => setTimeout(resolve, 1000));
    
    // Get the video element
    const videoElement = document.getElementById("videoResult");
    
    // Clear previous content
    videoElement.innerHTML = '';
    videoElement.style.display = "block";
    videoElement.style.width = "100%";
    videoElement.style.borderRadius = "14px";
    videoElement.controls = true;
    
    console.log("🎬 Video URL from backend:", data.video_url);
    
    // Setup event listeners BEFORE setting src
    videoElement.addEventListener('loadstart', () => {
      console.log("📡 Loading started...");
    });
    
    videoElement.addEventListener('loadedmetadata', () => {
      console.log("✅ Video metadata loaded successfully!");
      console.log("   Duration:", videoElement.duration, "seconds");
      console.log("   Width x Height:", videoElement.videoWidth, "x", videoElement.videoHeight);
      progressText.innerText = "✅ Video Ready!";
    });
    
    videoElement.addEventListener('canplay', () => {
      console.log("✅ Video can play!");
    });
    
    videoElement.addEventListener('error', (e) => {
      console.error("❌ Video error event:", e);
      console.error("   Error code:", videoElement.error ? videoElement.error.code : "unknown");
      console.error("   Error message:", videoElement.error ? videoElement.error.message : "unknown");
      console.error("   Failed URL:", data.video_url);
      console.error("   Current src:", videoElement.src);
      alert("Failed to load video. Check browser console for details.");
    });
    
    videoElement.addEventListener('stalled', () => {
      console.warn("⚠️  Video stalled");
    });
    
    // Set src directly on video element (NOT using source tag)
    console.log("📥 Setting video src directly...");
    videoElement.src = BACKEND_URL + data.video_url;
    videoElement.type = 'video/mp4';
    
    // Trigger load
    console.log("📥 Calling videoElement.load()...");
    videoElement.load();
    
    // Hide other results
    imageResult.style.display = "none";
    liveCanvas.style.display = "none";
    
    // Set counts
    setCounts(data.counts);
    
    // Hide progress bar after 2 seconds
    setTimeout(() => {
      progressContainer.style.display = "none";
      progressBar.style.width = "0%";
      progressPercent.innerText = "0%";
      progressText.innerText = "Processing...";
    }, 2000);
    
  } catch (error) {
    console.error("❌ Error during video processing:", error);
    clearInterval(progressInterval);
    progressContainer.style.display = "none";
    alert("Failed to process video. Check console for details.");
  } finally {
    detectBtn.disabled = false;
    detectBtn.innerText = "🎥 Detect Video";
  }
};

videoForm.file.onchange=(e)=>{
  videoFileName.innerText=e.target.files[0].name;
};

/* LIVE */
let stream=null;
startWebcamBtn.onclick=async()=>{
  stream = await navigator.mediaDevices.getUserMedia({
  video: { facingMode: "environment" }
  });

  liveVideo.srcObject=stream;
  startWebcamBtn.style.display="none";
  stopWebcamBtn.style.display="block";
  liveLoop();
};

stopWebcamBtn.onclick=()=>{
  stream.getTracks().forEach(t=>t.stop());
  startWebcamBtn.style.display="block";
  stopWebcamBtn.style.display="none";
};

async function liveLoop(){
  if(!stream) return;
  liveCanvas.width=liveVideo.videoWidth;
  liveCanvas.height=liveVideo.videoHeight;
  ctx.drawImage(liveVideo,0,0);

  liveCanvas.toBlob(async(b)=>{
    const fd=new FormData();
    fd.append("file",b,"frame.jpg");
    const res=await fetch(`${BACKEND_URL}/detect/image`,{method:"POST",body:fd});
    const data=await res.json();
    const img=new Image();
    img.onload=()=>ctx.drawImage(img,0,0);
    img.src=BACKEND_URL + data.image_url+"?t="+Date.now();
    liveCanvas.style.display="block";
    setCounts(data.counts);
  });

  setTimeout(liveLoop,800);
}

/* Update confidence value display */
document.getElementById("imageConf").oninput=(e)=>{
  document.getElementById("imageConfValue").innerText=parseFloat(e.target.value).toFixed(2);
};

document.getElementById("videoConf").oninput=(e)=>{
  document.getElementById("videoConfValue").innerText=parseFloat(e.target.value).toFixed(2);
};
