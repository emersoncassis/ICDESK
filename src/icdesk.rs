use base::config::keys;
use hbb_common::config::DEFAULT_SETTINGS;

/// Default server for this build, set at compile time with the `ICDESK_SERVER`
/// (host or host:port) and `ICDESK_KEY` (public key of the server) env vars.
/// They are defaults, so the user can still change them in the settings.
pub fn apply_default_server() {
    let server = option_env!("ICDESK_SERVER").unwrap_or_default().trim();
    if server.is_empty() {
        return;
    }
    let key = option_env!("ICDESK_KEY").unwrap_or_default().trim();
    let mut settings = DEFAULT_SETTINGS.write().unwrap();
    settings.insert(keys::OPTION_CUSTOM_RENDEZVOUS_SERVER.to_owned(), server.to_owned());
    if !key.is_empty() {
        settings.insert(keys::OPTION_KEY.to_owned(), key.to_owned());
    }
}
