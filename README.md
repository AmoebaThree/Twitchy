# Twitchy

The switch

## Message Spec

Format: \<channel> "message"

### Inputs

* \<twitchy> *
  * Triggers a request for status of the switch

### Outputs

* \<twitchy.switch> "switch.up"
  * The switch has been moved to the up position
  * Triggered automatically, or in response to a status query
* \<twitchy.switch> "switch.down"
  * The switch has been moved to the down position
  * Triggered automatically, or in response to a status query
* \<twitchy.switch.up> "up.on"
  * The switch has entered the up position
  * Triggered automatically, or in response to a status query
* \<twitchy.switch.up> "up.off"
  * The switch has left the up position
  * Triggered automatically, or in response to a status query
* \<twitchy.switch.down> "down.on"
  * The switch has entered the down position
  * Triggered automatically, or in response to a status query
* \<twitchy.switch.down> "down.off"
  * The switch has left the down position
  * Triggered automatically, or in response to a status query