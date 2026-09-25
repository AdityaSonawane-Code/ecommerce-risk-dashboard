const socket = io("http://127.0.0.1:5000");

let barChart, lineChart;
let timeLabels = [];

let failedData = [];
let successData = [];   // ✅ ADDED
let botData = [];

function initCharts() {

    // ✅ BAR CHART
    const ctx1 = document.getElementById("barChart").getContext("2d");
    barChart = new Chart(ctx1, {
        type: "bar",
        data: {
            labels: ["Failed", "Success", "Bots"],  // ✅ FIXED (removed undefined ones)
            datasets: [{
                label: "Attack Stats",
                data: [0, 0, 0],
                backgroundColor: ["red", "green", "orange"]
            }]
        },
        options: {
            responsive: true,
            plugins: {
                legend: { display: false }
            }
        }
    });

    // ✅ LINE CHART
    const ctx2 = document.getElementById("lineChart").getContext("2d");
    lineChart = new Chart(ctx2, {
        type: "line",
        data: {
            labels: timeLabels,
            datasets: [
                {
                    label: "Failed",
                    data: failedData,
                    borderColor: "red",
                    fill: false
                },
                {
                    label: "Success",   // ✅ ADDED
                    data: successData,
                    borderColor: "green",
                    fill: false
                },
                {
                    label: "Bots",
                    data: botData,
                    borderColor: "orange",
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            animation: false
        }
    });
}

socket.on("connect", () => {
    console.log("✅ Connected to backend");
});

socket.on("update", data => {

    console.log("📊 DATA:", data);

    // ✅ Safe values (avoid undefined)
    const failed = data.failed_logins || 0;
    const success = data.success_logins || 0;
    const bots = data.bot_detected || 0;

    // ✅ BAR CHART UPDATE
    barChart.data.datasets[0].data = [failed, success, bots];
    barChart.update();

    // ✅ LINE CHART UPDATE
    const time = new Date().toLocaleTimeString();

    timeLabels.push(time);
    failedData.push(failed);
    successData.push(success);   // ✅ ADDED
    botData.push(bots);

    // keep last 10 points
    if (timeLabels.length > 10) {
        timeLabels.shift();
        failedData.shift();
        successData.shift();   // ✅ ADDED
        botData.shift();
    }

    lineChart.update();

    // ✅ Suspicious IPs
    const sList = document.getElementById("suspicious");
    sList.innerHTML = "";
    (data.suspicious_ips || []).forEach(ip => {
        let li = document.createElement("li");
        li.textContent = ip;
        sList.appendChild(li);
    });

    // ✅ Bots list
    const bList = document.getElementById("bots");
    bList.innerHTML = "";
    (data.bots || []).forEach(ip => {
        let li = document.createElement("li");
        li.textContent = ip;
        bList.appendChild(li);
    });

    // ✅ Terminal Logs (now includes success)
    const logBox = document.getElementById("logs");
    let newLog = document.createElement("div");

    newLog.textContent = `[${time}] Failed:${failed} | Success:${success} | Bots:${bots}`;

    logBox.appendChild(newLog);
    logBox.scrollTop = logBox.scrollHeight;
});

// ✅ INIT
initCharts();