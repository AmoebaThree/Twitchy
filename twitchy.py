import systemd.daemon
import redis
import time


def execute():
    print('Startup')

    up_input = '4'
    down_input = '5'
    up_channel = 'pfd.input.' + up_input
    down_channel = 'pfd.input.' + down_input
    request_channel = 'twitchy'

    message_up_on = 'input.' + up_input + '.on'
    message_up_off = 'input.' + up_input + '.off'
    message_down_on = 'input.' + down_input + '.on'
    message_down_off = 'input.' + down_input + '.off'

    r = redis.Redis(host='192.168.0.1', port=6379,
                    db=0, decode_responses=True)
    p = r.pubsub(ignore_subscribe_messages=True)
    p.subscribe(request_channel, up_channel, down_channel)

    r.publish('services', 'twitchy.on')
    systemd.daemon.notify('READY=1')
    print('Startup complete')

    try:
        for message in p.listen():
            if message['channel'] == request_channel:
                r.publish('pfd.inputs', up_input)
                r.publish('pfd.inputs', down_input)

            elif message['channel'] == up_channel:
                if message['data'] == message_up_on:
                    r.publish('twitchy.switch', 'switch.up')
                    r.publish('twitchy.switch.up', 'up.on')
                elif message['data'] == message_up_off:
                    r.publish('twitchy.switch.up', 'up.off')

            elif message['channel'] == down_channel:
                if message['data'] == message_down_on:
                    r.publish('twitchy.switch', 'switch.down')
                    r.publish('twitchy.switch.down', 'down.on')
                elif message['data'] == message_down_off:
                    r.publish('twitchy.switch.down', 'down.off')
    except:
        p.close()
        r.publish('services', 'twitchy.off')
        print('Goodbye')


if __name__ == '__main__':
    execute()
