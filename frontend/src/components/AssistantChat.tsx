import { FormEvent, KeyboardEvent, useEffect, useRef, useState } from "react";
import { api } from "../api";
import { formatMarkdown } from "../constants";
import type { AssistantMessage } from "../types";

export default function AssistantChat() {
  const [messages, setMessages] = useState<AssistantMessage[]>([
    {
      role: "assistant",
      content: "Hi! I'm EcoGuide. Ask me about your footprint, get personalized tips, or learn how to reduce emissions.",
      suggested_actions: ["How am I doing?", "Tips to reduce my footprint", "Explain carbon footprint"],
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function sendMessage(text: string) {
    if (!text.trim() || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: text.trim() }]);
    setInput("");
    setLoading(true);

    try {
      const res = await api.chat(text.trim());
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.reply,
          suggested_actions: res.suggested_actions,
        },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Sorry, I couldn't reach the server. Make sure the backend is running." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleSubmit(e: FormEvent) {
    e.preventDefault();
    sendMessage(input);
  }

  function handleKeyDown(e: KeyboardEvent<HTMLInputElement>) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      sendMessage(input);
    }
  }

  return (
    <div className="card chat-container" aria-labelledby="assistant-heading">
      <h2 id="assistant-heading">EcoGuide Assistant</h2>
      <div className="chat-messages" role="log" aria-live="polite" aria-relevant="additions">
        {messages.map((msg, i) => (
          <div key={i}>
            <div className={`chat-bubble ${msg.role}`}>
              {msg.role === "assistant" ? (
                <span dangerouslySetInnerHTML={{ __html: formatMarkdown(msg.content) }} />
              ) : (
                msg.content
              )}
            </div>
            {msg.suggested_actions && msg.suggested_actions.length > 0 && (
              <div className="suggested-actions">
                {msg.suggested_actions.map((action) => (
                  <button key={action} className="chip" onClick={() => sendMessage(action)} disabled={loading}>
                    {action}
                  </button>
                ))}
              </div>
            )}
          </div>
        ))}
        {loading && <div className="chat-bubble assistant">Thinking…</div>}
        <div ref={bottomRef} />
      </div>
      <form className="chat-input-row" onSubmit={handleSubmit}>
        <label htmlFor="chat-input" className="sr-only">Message EcoGuide</label>
        <input
          id="chat-input"
          type="text"
          placeholder="Ask about your footprint…"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          disabled={loading}
          autoComplete="off"
        />
        <button type="submit" className="btn btn-primary" disabled={loading || !input.trim()}>
          Send
        </button>
      </form>
    </div>
  );
}
