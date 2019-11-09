import math
import time
import krpc


def main():
    print("running!")
    turn_start_altitude = 250
    turn_end_altitude = 45000
    target_altitude = 150000

    conn = krpc.connect(
        name='My Example Program',
        address='127.0.0.1',
        rpc_port=50000,
        stream_port=50001
    )
    vessel = conn.space_center.active_vessel
    print(vessel)

    # Set up streams for telemetry
    ut = conn.add_stream(getattr, conn.space_center, 'ut')
    altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
    apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
    stage_2_resources = vessel.resources_in_decouple_stage(stage=2, cumulative=False)
    srb_fuel = conn.add_stream(stage_2_resources.amount, 'SolidFuel')

    # Pre-launch setup
    vessel.control.sas = False
    vessel.control.rcs = False
    vessel.control.throttle = 1.0

    # Countdown...
    print('3...')
    time.sleep(1)
    print('2...')
    time.sleep(1)
    print('1...')
    time.sleep(1)
    print('Launch!')

    # Activate the first stage
    vessel.control.activate_next_stage()
    vessel.auto_pilot.engage()
    vessel.auto_pilot.target_pitch_and_heading(90, 90)

    # Main ascent loop
    srbs_separated = False
    turn_angle = 0
    while True:

        # Gravity turn
        if altitude() > turn_start_altitude and altitude() < turn_end_altitude:
            frac = ((altitude() - turn_start_altitude) /
                    (turn_end_altitude - turn_start_altitude))
            new_turn_angle = frac * 90
            if abs(new_turn_angle - turn_angle) > 0.5:
                turn_angle = new_turn_angle
                vessel.auto_pilot.target_pitch_and_heading(90 - turn_angle, 90)

        # Separate SRBs when finished
        if not srbs_separated:
            if srb_fuel() < 0.1:
                vessel.control.activate_next_stage()
                srbs_separated = True
                print('SRBs separated')

        # Decrease throttle when approaching target apoapsis
        if apoapsis() > target_altitude * 0.9:
            print('Approaching target apoapsis')
            break

if __name__ == '__main__':
    main()