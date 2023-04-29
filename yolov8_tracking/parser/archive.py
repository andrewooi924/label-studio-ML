def compute(file_path):
    cluster = {}
    seen = {}
    mapping = {}
    lines = read_file(file_path)

    # group lines by ID
    for line in lines:
        line = line.strip()
        frame_id, id, x, y, w, h, _, _, _, _, label, label_id = line.split(",")
        id, label_id = int(id), int(label_id)

        frame = FrameData(frame_id, id, x, y, w, h, label, label_id)

        if (id, label_id) not in cluster:
            cluster[(id, label_id)] = []
        cluster[(id, label_id)].append(frame)

    grouped_cluster = {}
    for (id, label_id), frames in cluster.items():
        # group continuous frames together
        groups = []
        group = []

        for frame in frames:
            if len(group) == 0:
                group.append(frame)
            else:
                prev_frame = group[-1]
                if prev_frame.frame_id + 1 == frame.frame_id:
                    group.append(frame)
                else:
                    groups.append(group)
                    group = [frame]

        groups.append(group)
        grouped_cluster[(id, label_id)] = groups

    for (id, label_id), groups in grouped_cluster.items():
        print(f"ID: {id}, Label ID: {label_id}")
        for group in groups:
            print("--------------------------------")
            for frame in group:
                print(frame, sep=" ")
        print("\n")
