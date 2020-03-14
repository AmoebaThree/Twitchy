if __name__ == '__main__':
    import systemd.daemon
    import redis
    import time

    up_input = '4'
    down_input = '5'
    up_channel = 'pfd.input.' + up_input
    down_channel = 'pfd.input.' + down_input
    request_channel = 'twitchy'

    print('Startup')
    r = redis.Redis(host='192.168.0.1', port=6379, db=0)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe(request_channel, up_channel, down_channel)
    print('Startup complete')
    systemd.daemon.notify('READY=1')

    try:
        for message in p.listen():
            if message.channel == request_channel:
                r.publish('pfd.inputs', up_input)
                r.publish('pfd.inputs', down_input)
            elif message.channel == up_channel:
                if message.message == "input." + up_input + ".on":
                    r.publish('twitchy.switch', 'switch.up')
                    r.publish('twitchy.switch.up', 'up.on')
                elif message.message == "input." + up_input + ".off":
                    r.publish('twitchy.switch.up', 'up.off')
            elif message.channel == down_channel:
                if message.message == "input." + down_input + ".on":
                    r.publish('twitchy.switch', 'switch.down')
                    r.publish('twitchy.switch.down', 'down.on')
                elif message.message == "input." + down_input + ".off":
                    r.publish('twitchy.switch.down', 'down.off')
    except:
        print("Goodbye")
