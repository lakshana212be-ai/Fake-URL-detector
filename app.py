import tkinter as tk
from tkinter import messagebox, scrolledtext
import joblib
import pandas as pd
from feature_extractor import extract_features
import os

# Load model
MODEL_PATH = "url_model.pkl"
try:
    model = joblib.load(MODEL_PATH)
except Exception as e:
    model = None
    print(f"Error loading model: {e}")

def check_urls(*args):
    if model is None:
        if 'messagebox' in globals(): messagebox.showerror("Error", "Model (url_model.pkl) not found. Please train first.")
        return
        
    # Get all lines from text area or argument
    if 'url_input' in globals():
        lines = url_input.get("1.0", tk.END).strip().split('\n')
    else:
        # CLI
        lines = args[0] if args else []
        
    urls = [line.strip() for line in lines if line.strip()]
    if not urls:
        if 'messagebox' in globals(): messagebox.showwarning("Warning", "Please enter at least one URL.")
        print("Please enter a URL.")
        return
        
    if 'result_text' in globals():
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        
    strict_mode = strict_var.get() if 'strict_var' in globals() else True

    for url in urls:
        # Auto-prefix missing protocols to ensure urlparse works correctly (like a modern browser)
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "https://" + url

        print(f"\nAnalyzing URL: {url} ...")
        
        # Explicitly mark HTTP as Unsafe
        if url.startswith("http://"):
            msg = f"[{url}]\nStatus: Unsafe ❌ | Safe Rate: 0.0% (Insecure Protocol)\n"
            if 'result_text' in globals():
                result_text.insert(tk.END, msg, "blocked")
                result_text.insert(tk.END, "-"*50 + "\n")
            print(msg.strip())
            continue

        # Extract features
        features = extract_features(url)
        df_features = pd.DataFrame([features])
        
        # Predict
        try:
            prediction = model.predict(df_features)[0]
            
            # Get probability
            safe_rate = 100.0
            threat_rate = 0.0
            if hasattr(model, "predict_proba"):
                proba = model.predict_proba(df_features)[0]
                if len(proba) > 1:
                    safe_rate = proba[0] * 100
                    threat_rate = proba[1] * 100
            
            if prediction == 0 and threat_rate < 30:
                msg = f"[{url}]\nStatus: Safe ✅ | Safe Rate: {safe_rate:.1f}%\n"
                if 'result_text' in globals():
                    result_text.insert(tk.END, msg, "safe")
                    result_text.insert(tk.END, "-"*50 + "\n")
            else:
                if threat_rate > 70:
                    msg = f"[{url}]\nStatus: Malicious ❌ | Threat Rate: {threat_rate:.1f}% (Safe Rate: {safe_rate:.1f}%)\n"
                    if 'result_text' in globals():
                        result_text.insert(tk.END, msg, "malicious")
                        result_text.insert(tk.END, "-"*50 + "\n")
                else:
                    msg = f"[{url}]\nStatus: Suspicious ⚠️ | Threat Rate: {threat_rate:.1f}% (Safe Rate: {safe_rate:.1f}%)\n"
                    if 'result_text' in globals():
                        result_text.insert(tk.END, msg, "suspicious")
                        result_text.insert(tk.END, "-"*50 + "\n")
            
            print(msg.strip())
            
        except Exception as e:
            if 'messagebox' in globals(): messagebox.showerror("Prediction Error", f"An error occurred during prediction:\n{e}")
            print(f"Prediction Error for {url}: {e}")
            
    if 'result_text' in globals():
        result_text.config(state=tk.DISABLED)

def refresh_ui():
    if 'url_input' in globals():
        url_input.delete("1.0", tk.END)
    if 'result_text' in globals():
        result_text.config(state=tk.NORMAL)
        result_text.delete("1.0", tk.END)
        result_text.insert(tk.END, "Status: Ready... Waiting for URLs to analyze.\n")
        result_text.config(state=tk.DISABLED)

if __name__ == "__main__":
    import sys
    
    if model is None:
        print("WARNING: url_model.pkl not found! Please run model_trainer.py first.")
    
    # Check if run as CLI
    if len(sys.argv) > 1:
        print("======== Google Office URL Safety Checker CLI ========")
        check_urls(sys.argv[1:])
    else:
        # GUI Setup - Material Design DARK Theme Inspired
        global root, url_input, result_text, strict_var
        
        root = tk.Tk()
        root.title("Google Office URL Safety Checker Pro - Dark Mode")
        root.geometry("750x650")
        root.configure(bg="#121212")

        # Fonts & Colors for Dark Theme
        FONT_TITLE = ("Segoe UI", 22, "bold")
        FONT_NORM = ("Segoe UI", 12)
        FONT_BOLD = ("Segoe UI", 12, "bold")
        COLOR_PRIMARY = "#8ab4f8" # Light blue for dark theme buttons
        COLOR_PRIMARY_HOVER = "#aecbfa"
        COLOR_CLEAR = "#3c4043"
        COLOR_BG = "#121212"
        COLOR_CARD = "#202124"
        FG_MAIN = "#e8eaed"
        FG_MUTED = "#9aa0a6"

        card = tk.Frame(root, bg=COLOR_CARD, padx=30, pady=25, relief="flat")
        card.pack(expand=True, fill="both", padx=20, pady=20)

        title_label = tk.Label(card, text="Enterprise URL Security", font=FONT_TITLE, bg=COLOR_CARD, fg=FG_MAIN)
        title_label.pack(pady=(0, 5))

        subtitle = tk.Label(card, text="Advanced AI-powered threat detection for Google Office (Bulk Mode)", font=("Segoe UI", 10), bg=COLOR_CARD, fg=FG_MUTED)
        subtitle.pack(pady=(0, 15))

        instruction_label = tk.Label(card, text="Enter Target URLs (One per line):", font=FONT_BOLD, bg=COLOR_CARD, fg=FG_MAIN, anchor="w")
        instruction_label.pack(fill="x")

        # Multi-line URLs Entry Box
        url_frame = tk.Frame(card, bg=COLOR_CARD)
        url_frame.pack(fill="x", pady=5)
        url_input = tk.Text(url_frame, font=FONT_NORM, bd=0, height=5, bg="#303134", fg=FG_MAIN, insertbackground=FG_MAIN, padx=10, pady=10)
        url_input.pack(fill="x")

        # Strict Mode Checkbox
        strict_var = tk.BooleanVar(value=True)
        strict_chk = tk.Checkbutton(card, text="Enable Google Office Strict HTTPS Mode", variable=strict_var, font=("Segoe UI", 10), 
                                    bg=COLOR_CARD, fg=FG_MAIN, activebackground=COLOR_CARD, activeforeground=FG_MAIN, selectcolor="#121212", cursor="hand2")
        strict_chk.pack(anchor="w", pady=(5, 10))

        # Button Frame (Side by side)
        btn_frame = tk.Frame(card, bg=COLOR_CARD)
        btn_frame.pack(pady=10)

        check_button = tk.Button(btn_frame, text="Analyze Security", font=FONT_BOLD, bg=COLOR_PRIMARY, fg="#202124", 
                                 activebackground=COLOR_PRIMARY_HOVER, activeforeground="#202124", width=18, pady=8, bd=0, cursor="hand2", command=check_urls)
        check_button.pack(side=tk.LEFT, padx=10)

        refresh_button = tk.Button(btn_frame, text="Refresh / Clear", font=FONT_BOLD, bg=COLOR_CLEAR, fg=FG_MAIN, 
                                 activebackground="#5f6368", activeforeground=FG_MAIN, width=15, pady=8, bd=0, cursor="hand2", command=refresh_ui)
        refresh_button.pack(side=tk.LEFT, padx=10)

        # Scrollable Results Area
        res_container = tk.Frame(card, bg="#303134", pady=10, padx=10)
        res_container.pack(expand=True, fill="both", pady=10)
        
        result_text = scrolledtext.ScrolledText(res_container, font=("Consolas", 11), bg="#303134", fg=FG_MAIN, bd=0, height=10)
        result_text.pack(expand=True, fill="both")
        
        # Configure text color tags
        result_text.tag_config("safe", foreground="#81c995") # Material Green Light
        result_text.tag_config("malicious", foreground="#f28b82") # Material Red Light
        result_text.tag_config("suspicious", foreground="#fdd663") # Material Yellow Light
        result_text.tag_config("blocked", foreground="#f28b82")
        
        refresh_ui() # Initialize text state

        if model is None:
            root.after(500, lambda: messagebox.showwarning("Model Missing", "url_model.pkl not found!\nPlease run model_trainer.py first to train the ML model."))
        
        print("======== Console Session Started (Waiting for UI Input) ========")
        root.mainloop()
