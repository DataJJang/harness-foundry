import { StrictMode } from "react";
import ReactDOM from "react-dom/client";
import { App } from "./App";
import "./styles.css";

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {
      // Keep bootstrap resilient even before a real offline strategy is added.
    });
  });
}

ReactDOM.createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <App />
  </StrictMode>
);
