async function fetchTasks() {
  const res = await fetch("/api/tasks");
  const tasks = await res.json();
  const list = document.getElementById("taskList");
  list.innerHTML = "";
  tasks.forEach(t => {
    const li = document.createElement("li");
    li.textContent = `${t.title} — ${t.description || ""} ${t.completed ? "✅" : ""}`;
    list.appendChild(li);
  });
}

async function addTask(title, desc) {
  if (!title) title = document.getElementById("title").value;
  if (!desc) desc = document.getElementById("desc").value;
  if (!title) return alert("Title required");
  await fetch("/api/tasks", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, description: desc })
  });
  fetchTasks();
}

async function generateTasks() {
  const prompt = document.getElementById("genPrompt").value;
  const count = parseInt(document.getElementById("genCount").value);
  const btn = document.getElementById("genBtn");
  btn.disabled = true;
  try {
    const res = await fetch("/api/tasks/autogen", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ prompt, n: count })
    });
    const tasks = await res.json();
    if (!res.ok) throw new Error(tasks.detail || "Failed");

    // 👇 Just refresh list, no need to call addTask again
    fetchTasks();

    alert(`Generated ${tasks.length} tasks successfully!`);
  } catch (e) {
    alert(`Autogen failed: ${e.message}`);
  } finally {
    btn.disabled = false;
  }
}

fetchTasks();
