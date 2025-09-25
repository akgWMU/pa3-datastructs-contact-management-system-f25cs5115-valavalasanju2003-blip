const base = "http://127.0.0.1:5000"; // Flask backend

function getDS() { 
  return document.getElementById("ds").value; 
}

function setOutput(text) {
  document.getElementById("output").textContent = text;
}

// Insert Contact
async function insertContact() {
  const name = document.getElementById("name").value.trim();
  const phone = document.getElementById("phone").value.trim();
  const email = document.getElementById("email").value.trim();

  if (!name) {
    setOutput("⚠️ Name is required.");
    return;
  }

  const res = await fetch(base + "/insert", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ds: getDS(), name, phone, email })
  });

  const data = await res.json();
  setOutput(JSON.stringify(data, null, 2));
}

// Search Contact
async function searchContact() {
  const target = document.getElementById("target").value.trim();
  if (!target) {
    setOutput("⚠️ Enter a name to search.");
    return;
  }

  const res = await fetch(base + `/search/${getDS()}/${encodeURIComponent(target)}`);
  const data = await res.json();
  setOutput(JSON.stringify(data, null, 2));
}

// Delete Contact
async function deleteContact() {
  const target = document.getElementById("target").value.trim();
  if (!target) {
    setOutput("⚠️ Enter a name to delete.");
    return;
  }

  const res = await fetch(base + `/delete/${getDS()}/${encodeURIComponent(target)}`, {
    method: "DELETE"
  });
  const data = await res.json();
  setOutput(JSON.stringify(data, null, 2));
}

// Update Contact
async function updateContact() {
  const oldName = document.getElementById("oldName").value.trim();
  const newName = document.getElementById("newName").value.trim();
  const newPhone = document.getElementById("newPhone").value.trim();
  const newEmail = document.getElementById("newEmail").value.trim();

  if (!oldName) {
    setOutput("⚠️ Enter the existing name of the contact to update.");
    return;
  }

  const payload = {
    ds: getDS(),
    old_name: oldName,
    new_name: newName || oldName,  // if new name not given, keep old one
    new_phone: newPhone,
    new_email: newEmail
  };

  const res = await fetch(base + "/update", {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload)
  });

  const data = await res.json();
  setOutput(JSON.stringify(data, null, 2));
}


// List Contacts
async function listContacts() {
  const res = await fetch(base + `/list/${getDS()}`);
  const data = await res.json();
  setOutput(JSON.stringify(data, null, 2));
}

// Run Benchmark
async function runBenchmark() {
  const n = document.getElementById("numOps").value || 2000;

  const res = await fetch(base + `/benchmark?n=${n}`);
  const blob = await res.blob();
  const imgUrl = URL.createObjectURL(blob);

  const img = document.getElementById("benchmarkImage");
  img.src = imgUrl;
  img.style.display = "block";

  setOutput(`Benchmark complete (n=${n}). Chart shown below.`);
  
}
async function runFullBenchmark() {
  setOutput("Running full benchmark...");
  const res = await fetch(base + "/full_benchmark");
  const data = await res.json();

  // Show theoretical complexities
  renderComplexityTable(data.complexities);

  // Show benchmark results
  renderBenchmarkTable(data.results);

  // Draw chart
  renderBenchmarkChart(data.results);

  setOutput("✅ Benchmark completed!");
}

function renderComplexityTable(complexities) {
  let html = `<h4>⏱️ Theoretical Complexities</h4><table border="1" class="styled-table"><tr><th>Data Structure</th><th>Insert</th><th>Search</th><th>Delete</th><th>List</th></tr>`;
  for (let ds in complexities) {
    html += `<tr>
      <td>${ds}</td>
      <td>${complexities[ds].insert}</td>
      <td>${complexities[ds].search}</td>
      <td>${complexities[ds].delete}</td>
      <td>${complexities[ds].list}</td>
    </tr>`;
  }
  html += `</table>`;
  document.getElementById("complexityTable").innerHTML = html;
}

function renderBenchmarkTable(results) {
  let html = `<h4>⚡ Experimental Results</h4><table border="1" class="styled-table"><tr>
    <th>Data Structure</th>
    <th>Size</th>
    <th>Insert Time (s)</th>
    <th>Search Time (s)</th>
    <th>Delete Time (s)</th>
    <th>List Time (s)</th>
    <th>Memory (KB)</th>
  </tr>`;
  results.forEach(r => {
    html += `<tr>
      <td>${r["Data Structure"]}</td>
      <td>${r["Size"]}</td>
      <td>${r["Insert Time (s)"].toFixed(6)}</td>
      <td>${r["Search Time (s)"].toFixed(6)}</td>
      <td>${r["Delete Time (s)"].toFixed(6)}</td>
      <td>${r["List Time (s)"].toFixed(6)}</td>
      <td>${r["Memory (KB)"].toFixed(2)}</td>
    </tr>`;
  });
  html += `</table>`;
  document.getElementById("benchmarkTable").innerHTML = html;
}

function renderBenchmarkChart(results) {
  const ctx = document.getElementById("benchmarkChart").getContext("2d");

  // Group data by operation
  const operations = ["Insert Time (s)", "Search Time (s)", "Delete Time (s)", "List Time (s)"];
  const sizes = [...new Set(results.map(r => r.Size))];

  const datasets = operations.map(op => ({
    label: op,
    data: sizes.map(size => {
      // avg across data structures
      const filtered = results.filter(r => r.Size === size);
      return filtered.reduce((sum, r) => sum + r[op], 0) / filtered.length;
    }),
    fill: false,
    borderWidth: 2
  }));

  new Chart(ctx, {
    type: "line",
    data: {
      labels: sizes,
      datasets: datasets
    },
    options: {
      responsive: true,
      plugins: {
        title: {
          display: true,
          text: "Benchmark Performance (Average across DS)"
        }
      },
      scales: {
        y: { beginAtZero: true }
      }
    }
  });
}
