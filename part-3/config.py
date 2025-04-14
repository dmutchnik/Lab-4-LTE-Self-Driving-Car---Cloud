class Config:
    def __init__(self):
        self.delivery_stream_name = "cs437_lab4_stream_put"
        self.region = "us-west-2"
        self.sample_data_file = (
            "../data/vehicle0.csv"
        )


def get_config():
    return Config()