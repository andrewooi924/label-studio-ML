class FrameData:
    def __init__(self, frame_id, id, x, y, w, h, label, label_id):
        self.frame_id = int(frame_id)
        self.id = int(id)
        self.x = float(x)
        self.y = float(y)
        self.w = float(w)
        self.h = float(h)

        # Capitalize the first letter of the label
        self.label = label.capitalize()
        self.label_id = int(label_id)

    def generate_frame_json(self, interpolation=False):
        return {
            "frame": self.frame_id,
            "x": self.x,
            "y": self.y,
            "width": self.w,
            "height": self.h,
            "enabled": interpolation,
        }

    def __str__(self):
        # Should be in JSON format
        return f"frame_id: {self.frame_id}, id: {self.id}, x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}, label: {self.label}, label_id: {self.label_id}"


class Compute:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def _read_file(self):
        with open(self.file_path) as f:
            lines = f.readlines()
        return lines

    def _group_by_id(self, lines):
        cluster = {}
        for line in lines:
            line = line.strip()
            frame_id, id, x, y, w, h, _, _, _, _, label, label_id = line.split(",")
            frame = FrameData(frame_id, id, x, y, w, h, label, label_id)

            # Grouping by two keys, namely frame_id and label_id
            if (frame.id, frame.label_id) not in cluster:
                cluster[(frame.id, frame.label_id)] = []
            cluster[(frame.id, frame.label_id)].append(frame)
        return cluster

    def _group_by_continuous_frames(self, cluster):
        grouped_cluster = {}
        for (id, label_id), frames in cluster.items():
            groups, group = [], []
            for i, frame in enumerate(frames):
                if i == 0:
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
        return grouped_cluster

    def _generate_ls_json(self, grouped_cluster):
        results = []
        for (id, label_id), groups in grouped_cluster.items():
            sequence = []
            obj_name = None
            for group in groups:
                for i in range(len(group)):
                    frame = group[i]

                    if obj_name is None:
                        obj_name = frame.label

                    if len(group) == 1:
                        sequence.append(frame.generate_frame_json(interpolation=False))
                        continue
                    is_last = i == len(group) - 1
                    sequence.append(frame.generate_frame_json(interpolation=(not is_last)))

            results.append(
                {
                    "value": {"sequence": sequence, "labels": [obj_name]},
                    "from_name": "box",
                    "to_name": "video",
                    "type": "videorectangle",
                    "origin": "yolov8",
                }
            )
        return {"result": results}

    def process(self):
        lines = self._read_file()
        cluster = self._group_by_id(lines)
        grouped_cluster = self._group_by_continuous_frames(cluster)
        json_result = self._generate_ls_json(grouped_cluster)
        return json_result

    def pretty_print_grouped_cluster(self, grouped_cluster):
        for (id, label_id), groups in grouped_cluster.items():
            print(f"ID: {id}, Label ID: {label_id}")
            for group in groups:
                print("--------------------------------")
                for frame in group:
                    print(frame, sep=" ")
            print("\n")
