<script>
async function sendPrompt() {
  const prompt = document.getElementById("prompt").value;
  const responseBox = document.getElementById("response");

  console.log("Sending prompt:", prompt);
  responseBox.innerText = "Loading...";

  try {
    const res = await fetch("http://127.0.0.1:8000/generate-jd", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ role_details: prompt })
    });

    console.log("HTTP status:", res.status);

    const data = await res.json();
    console.log("Response data:", data);

    responseBox.innerText = data.job_description;
  } catch (err) {
    console.error(err);
    responseBox.innerText = "Error: " + err.message;
  }
}
</script>
