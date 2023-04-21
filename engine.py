from label_studio_ml.model import LabelStudioMLBase
import random

""" Assisted Bounding Box labelling
1. This model helps our frontend to label the videos with the generated bounding boxes for the frontend. 
2. The format of the prediction is as follows

{
  "value": {
    "framesCount": number, total frames in video
    "duration": number, total duration of video
    "sequence": [
      {
        "frame": number,
        "rotation": number,
        "x": number,
        "y": number,
        "width": number,
        "height": number,
        "time": number
      },
      {
        "x": number,
        "y": number,
        "width": number,
        "height": number,
        "rotation": number,
        "frame": number,
        "time": number
      }
    ],
    "labels": string[]
  },
  "id": string,
  "from_name": string,
  "to_name": string,
  "type": string,
  "origin": string
  }
}

"""
class AssistedBoundingBox(LabelStudioMLBase):
    def __init__(self, **kwargs):
        # don't forget to call base class constructor
        super(AssistedBoundingBox, self).__init__(**kwargs)
    
        # you can preinitialize variables with keys needed to extract info from tasks and annotations and form predictions
        from_name, schema = list(self.parsed_label_config.items())[0]
        self.from_name = from_name
        self.to_name = schema['to_name'][0]
        self.labels = schema['labels']

    def _run_tracker(self, vid_url):
        
        # Video URL is passed onto the tracker
        # Saves to ROOT / runs / track / exp /
        try:
          command = f"python3 yolov8_tracking/track.py --source ${vid_url} --save-txt" 
          
          # Run process to track the video
          subprocess.run(command.split(), check=True)

          # Get the path of the generated file
          path = f"runs/track/exp/{vid_url.split('/')[-1].split('.')[0]}.txt"

          # Read the file
          with open(path, 'r') as f:
            data = f.readlines()
            print(data)

        except Exception as e:
          print("Error in running tracker with error: " + e)

    def predict(self, tasks, **kwargs):
        """ This is where inference happens: model returns 
            the list of predictions based on input list of tasks 
        """
        predictions = []
        print(kwargs)
        for task in tasks:
            predictions.append({
                'result': [{
                    'from_name': self.from_name,
                    'to_name': self.to_name,
                    'type': 'choices',
                    'value': {
                        'choices': [random.choice(self.labels)]
                    }
                }],
                'score': 1
            })
        
        return predictions