/**
 * Session Kickoff Extension
 *
 * Sends "Bonjour" on new sessions to trigger the AGENTS.md workflow.
 */

import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";

export default function (pi: ExtensionAPI) {
  pi.on("session_start", async (event) => {
    if (event.reason === "startup" || event.reason === "new") {
      pi.sendUserMessage("Bonjour");
    }
  });
}
