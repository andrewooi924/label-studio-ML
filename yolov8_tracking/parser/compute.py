class FrameData:
    def __init__(self, frame_id, id, x, y, w, h, label, label_id):
        self.frame_id = int(frame_id)
        self.id = int(id)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.label = label
        self.label_id = int(label_id)

    def __str__(self):
        # Should be in JSON format
        return f"frame_id: {self.frame_id}, id: {self.id}, x: {self.x}, y: {self.y}, w: {self.w}, h: {self.h}, label: {self.label}, label_id: {self.label_id}"


class Compute:
    def __init__(self, file_path=None):
        self.file_path = file_path

    def _read_file(self):
        with open(file_path) as f:
            lines = f.readlines()
        return lines

    def _group_by_id(self, lines):
        cluster = {}
        for line in lines:
            line = line.strip()
            frame_id, id, x, y, w, h, _, _, _, _, label, label_id = line.split(",")
            frame = FrameData(frame_id, id, x, y, w, h, label, label_id)
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

    def process(self):
        lines = self._read_file()
        cluster = self._group_by_id(lines)
        grouped_cluster = self._group_by_continuous_frames(cluster)
        return grouped_cluster

    def pretty_print(self, grouped_cluster):
        for (id, label_id), groups in grouped_cluster.items():
            print(f"ID: {id}, Label ID: {label_id}")
            for group in groups:
                print("--------------------------------")
                for frame in group:
                    print(frame, sep=" ")
            print("\n")


if __name__ == "__main__":
    file_path = "test.txt"
    compute = Compute(file_path=file_path)
    res = compute.process()
    compute.pretty_print(res)
