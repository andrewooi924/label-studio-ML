from label_studio_ml.model import LabelStudioMLBase

class PredictionModel(LabelStudioMLBase):
    def __init__(self, **kwargs):
        # don't forget to call base class constructor
        super(DummyModel, self).__init__(**kwargs)
    
        # you can preinitialize variables with keys needed to extract info from tasks and annotations and form predictions
        from_name, schema = list(self.parsed_label_config.items())[0]
        self.from_name = from_name
        self.to_name = schema['to_name'][0]
        self.labels = schema['labels']

    def predict(self, tasks, **kwargs):
        """ This is where inference happens: model returns 
            the list of predictions based on input list of tasks 
        """
        print('task', tasks)
        predictions = []
        for task in tasks:
            predictions.append({
                'score': 0.987,  # prediction overall score, visible in the data manager columns
                'model_version': 'delorean-20151021',  # all predictions will be differentiated by model version
                'result': [{
          "original_length": 90.975,
          "value": {
            "start": 7.364642857142857,
            "end": 26.317767857142858,
            "channel": 0,
            "labels": [
              "Selection 1"
            ]
          },
          "id": "RmCN8",
          "from_name": "caption",
          "to_name": "audio",
          "type": "labels",
          "origin": "manual"
        },
        {
          "original_length": 90.975,
          "value": {
            "start": 7.364642857142857,
            "end": 26.317767857142858,
            "channel": 0,
            "text": [
              "this is something"
            ]
          },
          "id": "RmCN8",
          "from_name": "transcription",
          "to_name": "audio",
          "type": "textarea",
          "origin": "manual"
        },
        {
          "original_length": 90.975,
          "value": {
            "start": 36.17339285714285,
            "end": 60.216785714285706,
            "channel": 0,
            "labels": [
              "Selection 2"
            ]
          },
          "id": "y9S0H",
          "from_name": "caption",
          "to_name": "audio",
          "type": "labels",
          "origin": "manual"
        },
        {
          "original_length": 90.975,
          "value": {
            "start": 36.17339285714285,
            "end": 60.216785714285706,
            "channel": 0,
            "text": [
              "this is another"
            ]
          },
          "id": "y9S0H",
          "from_name": "transcription",
          "to_name": "audio",
          "type": "textarea",
          "origin": "manual"
        },
        {
          "value": {
            "framesCount": 2183.3999999999996,
            "duration": 90.975011,
            "sequence": [
              {
                "frame": 1,
                "rotation": 0,
                "x": 42.8125,
                "y": 51.24999999999999,
                "width": 12.5,
                "height": 25,
                "time": 0.041666666666666664
              },
              {
                "x": 42.308932360204196,
                "y": 51.72466015192493,
                "width": 12.499999999999952,
                "height": 25.000000000000128,
                "rotation": -3.1363583683323393,
                "frame": 7,
                "time": 0.2916666666666667
              }
            ],
            "labels": [
              "Woman"
            ]
          },
          "id": "S8pNPjXnzJ",
          "from_name": "box",
          "to_name": "video",
          "type": "videorectangle",
          "origin": "manual"
        }]
            })
        return predictions