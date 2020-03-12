if __name__ == '__main__':
    import systemd.daemon
    import pifacedigitalio
    import redis
    import time

    print('Startup')
    pfd = pifacedigitalio.PiFaceDigital()
    listener = pifacedigitalio.InputEventListener(chip=pfd)
    r = redis.Redis(host='192.168.0.1', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe('twitchy')
    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        def up_on(e):
            r.publish("twitchy-switch", "switch-up")
            r.publish("twitchy-switch-up", "up-on")

        def up_off(e):
            r.publish("twitchy-switch-up", "up-off")

        def down_on(e):
            r.publish("twitchy-switch", "switch-down")
            r.publish("twitchy-switch-down", "down-on")

        def down_off(e):
            r.publish("twitchy-switch-down", "down-off")

        listener.register(4, pifacedigitalio.IODIR_FALLING_EDGE, up_on)
        listener.register(4, pifacedigitalio.IODIR_RISING_EDGE, up_off)
        listener.register(5, pifacedigitalio.IODIR_FALLING_EDGE, down_on)
        listener.register(5, pifacedigitalio.IODIR_RISING_EDGE, down_off)
        listener.activate()

        for message in p.listen():
            # If message is received, send current status
            if pfd.input_pins[4].value > 0:
                up_on(None)
            elif pfd.input_pins[5].value > 0:
                down_on(None)
    except:
        listener.deactivate()
        pfd.deinit_board()
        print("Goodbye")
