# thanks AI - GLM-4.7

import math
import random
import time


def generate_mouse_data(
    num_points=5,
    x_range=(500, 800),
    y_range=(300, 400),
    include_click=True,
    target_element="TWICKETS-BUY-OVERVIEW",
    device_capability="desktop",
):
    """
    Generate synthetic mouse tracking data for research purposes.

    Args:
        num_points: Number of movement points to generate
        x_range: Tuple of (min_x, max_x) for coordinates
        y_range: Tuple of (min_y, max_y) for coordinates
        include_click: Whether to include click events in collector3
        target_element: Target element name for click events
        device_capability: Device type string ("desktop" or "mobile")

    Returns:
        Dictionary with collector1, collector2, collector3, and deviceCapability
    """

    # Current timestamp in milliseconds
    base_timestamp = int(time.time() * 1000)

    # ============================================
    # Collector1: Mouse movement data
    # ============================================
    collector1 = []

    # Starting position
    prev_x = random.uniform(*x_range)
    prev_y = random.uniform(*y_range)

    # Simulate an implied previous point for initial velocity
    implied_prev_x = prev_x - random.gauss(8, 4)
    implied_prev_y = prev_y - random.gauss(8, 4)

    current_timestamp = base_timestamp

    # Generate a general direction for this movement burst
    direction_x = random.choice([-1, 1]) * random.uniform(3, 8)
    direction_y = random.choice([-1, 1]) * random.uniform(3, 8)

    for i in range(num_points):
        # Add some randomness to movement (natural jitter)
        jitter_x = random.gauss(0, 2)
        jitter_y = random.gauss(0, 2)

        dx = direction_x + jitter_x
        dy = direction_y + jitter_y

        new_x = prev_x + dx
        new_y = prev_y + dy

        # Clamp to bounds
        new_x = max(x_range[0], min(x_range[1], new_x))
        new_y = max(y_range[0], min(y_range[1], new_y))

        # Time delta (typical mouse polling: 1-16ms, with occasional gaps)
        if i == 0:
            time_delta = random.randint(8, 15)
            # Calculate velocity from implied previous point
            calc_dx = prev_x - implied_prev_x
            calc_dy = prev_y - implied_prev_y
        else:
            # Occasionally have shorter or longer intervals
            if random.random() < 0.2:  # 20% chance of short interval
                time_delta = random.randint(2, 5)
            else:
                time_delta = random.randint(8, 16)
            calc_dx = dx
            calc_dy = dy

        current_timestamp += time_delta

        # Calculate velocity: pixels per second
        distance = math.sqrt(calc_dx**2 + calc_dy**2)
        dt_seconds = time_delta / 1000
        velocity = distance / dt_seconds if dt_seconds > 0 else 0

        collector1.append(
            {
                "x": round(new_x),
                "y": round(new_y),
                "timestamp": current_timestamp,
                "velocity": velocity,
            }
        )

        prev_x = new_x
        prev_y = new_y

    # ============================================
    # Collector2: Typically empty
    # ============================================
    collector2 = []

    # ============================================
    # Collector3: Click event data
    # ============================================
    collector3 = []

    if include_click:
        # Click coordinates (can be 0 if clicking on edge/scrollbar area)
        if random.random() < 0.3:
            click_x = 0  # Edge click like in your example
        else:
            click_x = round(random.uniform(*x_range))
        click_y = round(random.uniform(*y_range))

        # Click happens before movement data typically
        click_timestamp = base_timestamp - random.randint(3000, 5000)

        # mousedown event
        collector3.append(
            {
                "x": click_x,
                "y": click_y,
                "timestamp": click_timestamp,
                "eventType": "mousedown",
                "button": 0,
                "targetElement": target_element,
                "ctrlKey": False,
                "shiftKey": False,
                "altKey": False,
            }
        )

        # mouseup event (50-150ms after mousedown for natural click)
        mouseup_delay = random.randint(50, 150)
        collector3.append(
            {
                "x": click_x,
                "y": click_y,
                "timestamp": click_timestamp + mouseup_delay,
                "eventType": "mouseup",
                "button": 0,
                "targetElement": target_element,
                "ctrlKey": False,
                "shiftKey": False,
                "altKey": False,
            }
        )

        # click event (same timestamp as mouseup)
        collector3.append(
            {
                "x": click_x,
                "y": click_y,
                "timestamp": click_timestamp + mouseup_delay,
                "eventType": "click",
                "button": 0,
                "targetElement": target_element,
                "ctrlKey": False,
                "shiftKey": False,
                "altKey": False,
            }
        )

    return {
        "collector1": collector1,
        "collector2": collector2,
        "collector3": collector3,
        "deviceCapability": device_capability,
    }
