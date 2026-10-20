// Simple client-side rate limiting for form-like interactions (if any)
// and helps with 404 page behavior if hosted with routing

const RATE_LIMIT_KEY = "doom_py_last_req";
const RATE_LIMIT_MS = 2000; // 2 seconds simple throttle

function isRateLimited() {
  const now = Date.now();
  const last = parseInt(localStorage.getItem(RATE_LIMIT_KEY) || "0");
  if (now - last < RATE_LIMIT_MS) return true;
  localStorage.setItem(RATE_LIMIT_KEY, String(now));
  return false;
}

// gentle throttle on link clicks if needed
document.addEventListener("click", (e) => {
  const t = e.target;
  if (t.tagName === "A" && isRateLimited()) {
    e.preventDefault();
  }
});
