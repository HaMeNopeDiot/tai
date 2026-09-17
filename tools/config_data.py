from pathlib import Path
from dataclasses import dataclass

@dataclass
class ConfigData:
    filename: Path  = ".config"
    api_key: str = None
    model: str = None
    base_url:str = None
    temperature:float = None

    def parse_config(self):
        # Initialize an empty dictionary to hold your key-value pairs
        data_dict = {}
        # Open and read the file
        with open(self.filename, "r", encoding="utf-8") as file:
            for line in file:
                # Strip whitespace from the beginning and end of the line
                line = line.strip()

                # Skip empty lines and comments (lines starting with #)
                if not line or line.startswith("#"):
                    continue

                # Split the line by the first '=' character
                if "=" in line:
                    name, val = line.split("=", 1)

                    # Clean up extra whitespace around names and values
                    data_dict[name.strip()] = val.strip()
        self.api_key = data_dict['API_KEY']
        self.model = data_dict['MODEL']
        self.base_url = data_dict['BASE_URL']
        self.temperature = float(data_dict['TEMPERATURE'])


if __name__ == "__main__":
    cfgdata = ConfigData()
    cfgdata.parse_config()

    print(f"{cfgdata.api_key} ({type(cfgdata.api_key)})")
    print(f"{cfgdata.model} ({type(cfgdata.model)})")
    print(f"{cfgdata.base_url} ({type(cfgdata.base_url)})")
    print(f"{cfgdata.temperature} ({type(cfgdata.temperature)})")