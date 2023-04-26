#This file does 3 thing
#   1)Reads in json data from an input file
#   2)Parses json data from that input file per a given set of search criteria 
#   3)Takes matches and writes them to an output file
#
# ---Author: Justin Dyer---

import json
from datetime import datetime
from pathlib import Path

class Filter:
    
    def __init__(self):
        #Store matches in self object 
        self.matches = []

    def filter(
        self,
        input_file,
        bounding_box,
        capacity_range,
        output_file,
        date_range =("0001-01-01", "9999-12-31") #Since date is an optional param, a default range is supplied
    ):
        
        #Check to see if file exists
        input_file = Path(input_file)
        if not input_file.exists() or not input_file.is_file():
            raise FileNotFoundError(f"Invalid input file {input_file!r}")
        input_data = json.load(input_file.open("r"))
        
        #Check bounding box for proper stucture and number of args
        if not isinstance (bounding_box, list) or len(bounding_box) != 4:
            raise ValueError('Invalid input for bounding_box.')  
        horz_lower, vert_lower, horz_upper, vert_upper = bounding_box 
        
        #Check capacity range for proper stucture and number of args
        if not isinstance (capacity_range, tuple) or len(capacity_range) != 2:
            raise ValueError('Invalid input for capacity_range')
        cap_lower, cap_upper  = capacity_range 
    
        #Check date for proper structure
        if not isinstance (date_range, tuple):
            raise ValueError('Invalid input for date_range')
        start_date, end_date = date_range
        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        
        #Filter for objects that match search criteria 
        for data in input_data:
            if(
                horz_lower <= data.get('horizontal')<= horz_upper
                and vert_lower <= data.get('vertical')<= vert_upper
                and cap_lower <= data.get('capacity')<= cap_upper
                and start_date <= datetime.strptime(data.get('date'), '%Y-%m-%d')<= end_date
            ):
                self.matches.append(data)
            
        #Write matches to output file
        if self.matches:
            with Path(output_file).open("w") as o:
                json.dump(self.matches, o, indent=0)
            
def main():   
    input_file, output_file = "Input.json", "Output.json"

    f = Filter()
    #Sample input 
    f.filter(        
        input_file=input_file,
        bounding_box=[-90.0, -180.0, 90.0, 180.0],
        capacity_range=(0.0, 10.0),
        date_range= ('2021-04-10', '2023-03-14'),
        output_file=output_file,
    )

    print(f'Wrote to {output_file}')
    
if __name__ == "__main__":
    main()
