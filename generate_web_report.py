from utils.lib_general_utils import Utils

class GenerateWebReport:

    def __init__(self, report_dict: dict, save_file_location: str):
        super().__init__()
        self.util_obj = Utils()
        self.save_file_location = save_file_location
        self.system_report = report_dict
        self.file_content = """<!DOCTYPE html>
        <html>
        <head>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
        <style>
        body {
            font-family: "Lato", sans-serif;
        }

        /* Fixed sidenav, full height */
        .sidenav {
            height: 100%;
            width: 200px;
            position: fixed;
            z-index: 1;
            top: 0;
            left: 0;
            background-color: #111;
            overflow-x: hidden;
            padding-top: 20px;
        }

        /* Style the sidenav links and the dropdown button */
        .sidenav a, .dropdown-btn {
            padding: 6px 8px 6px 16px;
            text-decoration: none;
            font-size: 20px;
            color: #818181;
            display: block;
            border: none;
            background: none;
            width: 100%;
            text-align: left;
            cursor: pointer;
            outline: none;
        }

        /* On mouse-over */
        .sidenav a:hover, .dropdown-btn:hover {
            color: #f1f1f1;
        }

        /* Main content */
        .main {
            margin-left: 200px; /* Same as the width of the sidenav */
            font-size: 20px; /* Increased text to enable scrolling */
            padding: 0px 10px;
        }

        /* Add an active class to the active dropdown button */
        .active {
            background-color: green;
            color: white;
        }

        /* Dropdown container (hidden by default). Optional: add a lighter background color and some left padding to change the design of the dropdown content */
        .dropdown-container {
            display: none;
            background-color: #262626;
            padding-left: 8px;
        }

        /* Optional: Style the caret down icon */
        .fa-caret-down {
            float: right;
            padding-right: 8px;
        }

        /* Some media queries for responsiveness */
        @media screen and (max-height: 450px) {
            .sidenav {padding-top: 15px;}
            .sidenav a {font-size: 18px;}
        }
        </style>
        </head>
        <body>
        <div class="sidenav">
            <button class="dropdown-btn">Web Report 
                <i class="fa fa-caret-down"></i>
            </button>
            <div class="dropdown-container">
        """


    def parse_result(self):
        # Add keys to side nav bar
        for key in self.system_report.keys():
            self.file_content += f"<a href='#'>{key}</a>"

        keys = []
        
        ## parse for keyss
        for key in self.system_report.keys():
            if key == "result" or key == "args":
                pass
            else:
                
        
        
        
        self.file_content += """
                </div>
            </div>

                <div class="main">
                <h2>SECURUS AUDIRE</h2>
            """

        for key, value in self.system_report.items():
            if 

        # add content for that particular key
        self.file_content += """
                <script>
                /* Loop through all dropdown buttons to toggle between hiding and showing its dropdown content - This allows the user to have multiple dropdowns without any conflict */
                    var dropdown = document.getElementsByClassName("dropdown-btn");
                    var i;

                    for (i = 0; i < dropdown.length; i++) {
                    dropdown[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var dropdownContent = this.nextElementSibling;
                    if (dropdownContent.style.display === "block") {
                    dropdownContent.style.display = "none";
                    } else {
                    dropdownContent.style.display = "block";
                    }
                    });
                    }
                </script>
                <script>
                        function myFunc(id){
                        if (document.getElementById(id.concat("_content")).style.display == "none") {
                            document.getElementById(id.concat("_content")).style.display = "table-row";
                        } else {
                                document.getElementById(id.concat("_content")).style.display = "none";
                            } 
                        }
                </script>

            </body>
            </html> """

    def create_file(self):
        
        if not self.util_obj.check_file_exsists(self.save_file_location+"/SecurusAudire_Reports"):
            self.util_obj.get_command_output(['mkdir', self.save_file_location+'/SecurusAudire_Reports'])

        timestamp = self.util_obj.get_current_datetime()
        with open(self.save_file_location+"/SecurusAudire_Reports/web_report-"+self.util_obj.get_current_datetime()+".html", 'w+') as write_file_obj:
            write_file_obj.write(self.file_content)
    
    def generate_report(self):
        self.parse_result()
        self.create_file()
