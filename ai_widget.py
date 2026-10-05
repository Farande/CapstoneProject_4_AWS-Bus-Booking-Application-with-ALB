"""Injects the small floating AI-assistant popup into every HTML page.
Kept isolated so a bug here can never take down an unrelated route."""

POPUP_HTML = '''
    <div data-ai-popup="1" class="ai-assistant-widget" id="aiAssistantWidget">
        <button class="ai-assistant-toggle" id="aiAssistantToggle" type="button" aria-label="Open AI assistant">
            <span>AI</span>
        </button>

        <div class="ai-assistant-panel" id="aiAssistantPanel" aria-hidden="true">
            <div class="ai-assistant-header">
                <div>
                    <p class="eyebrow">Smart help</p>
                    <h3>AI Travel Assistant</h3>
                </div>
                <button type="button" class="ai-assistant-close" id="aiAssistantClose" aria-label="Close assistant">×</button>
            </div>

            <div class="ai-assistant-message">
                <strong>Need help with your trip?</strong>
                <p>Check routes, seat availability, boarding timing, and service updates in one place.</p>
            </div>

            <div class="ai-assistant-actions">
                <button type="button" class="ai-assistant-action">Best route</button>
                <button type="button" class="ai-assistant-action">Seat advice</button>
                <button type="button" class="ai-assistant-action">Delay check</button>
            </div>

            <a href="/assistant" class="ai-assistant-link">Open full assistant</a>
        </div>
    </div>

    <script>
        (function () {
            const widget = document.getElementById('aiAssistantWidget');
            const panel = document.getElementById('aiAssistantPanel');
            const toggle = document.getElementById('aiAssistantToggle');
            const closeBtn = document.getElementById('aiAssistantClose');

            if (!widget || !panel || !toggle) return;

            toggle.addEventListener('click', function () {
                const isOpen = panel.classList.contains('open');
                panel.classList.toggle('open', !isOpen);
                panel.setAttribute('aria-hidden', String(isOpen));
            });

            if (closeBtn) {
                closeBtn.addEventListener('click', function () {
                    panel.classList.remove('open');
                    panel.setAttribute('aria-hidden', 'true');
                });
            }
        })();
    </script>
    '''


def register_ai_widget(app):
    @app.after_request
    def inject_ai_assistance(response):
        if response.mimetype != "text/html" or response.is_json:
            return response

        try:
            html = response.get_data(as_text=True)
        except Exception:
            return response

        if "data-ai-popup" in html:
            return response

        if "</body>" in html:
            html = html.replace("</body>", POPUP_HTML + "\n</body>", 1)
            response.set_data(html)

        return response
