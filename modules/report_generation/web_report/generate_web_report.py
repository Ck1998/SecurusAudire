from modules.report_generation.report_generator_base import ReportGenBase
from os import makedirs
from config import CURR_SYSTEM_PLATFORM


class GenerateWebReport(ReportGenBase):

    def __init__(self, full_report: dict, save_folder_location: str, timestamp):
        super().__init__()
        self.save_folder_location = save_folder_location
        self.full_report = full_report
        self.audit_result = self.full_report["Audit Results"]
        self.timestamp = timestamp
        self.file_content = """<!DOCTYPE html><html><head> <meta charset="utf-8"> <meta name="viewport" 
        content="width=device-width, initial-scale=1.0"> <meta http-equiv="X-UA-Compatible" content="IE=edge"> 
        <title>SecureAudire Web Report</title> <style>/* DEMO STYLE*/@import 
        "https://fonts.googleapis.com/css?family=Poppins:300,400,500,600,700";body{font-family: "Poppins", 
        sans-serif; background: #fafafa;}p{font-family: "Poppins", sans-serif; font-size: 1.1em; font-weight: 300; 
        line-height: 1.7em; color: #999;}a,a:hover,a:focus{color: inherit; text-decoration: none; transition: all 
        0.3s;}.navbar{padding: 15px 10px; background: #fff; border: none; border-radius: 0; margin-bottom: 40px; 
        box-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);}.navbar-btn{box-shadow: none; outline: none !important; border: 
        none;}.line{width: 100%; height: 1px; border-bottom: 1px dashed #ddd; margin: 40px 0;}/* 
        --------------------------------------------------- SIDEBAR 
        STYLE----------------------------------------------------- */#sidebar{width: 250px; position: fixed; top: 0; 
        left: -250px; height: 100vh; z-index: 999; background: #7386D5; color: #fff; transition: all 0.3s; 
        overflow-y: scroll; box-shadow: 3px 3px 3px rgba(0, 0, 0, 0.2);}#sidebar.active{left: 0;}#dismiss{width: 
        35px; height: 35px; line-height: 35px; text-align: center; background: #7386D5; position: absolute; top: 
        10px; right: 10px; cursor: pointer; -webkit-transition: all 0.3s; -o-transition: all 0.3s; transition: all 
        0.3s;}#dismiss:hover{background: #fff; color: #7386D5;}.overlay{display: none; position: fixed; width: 100vw; 
        height: 100vh; background: rgba(0, 0, 0, 0.7); z-index: 998; opacity: 0; transition: all 0.5s 
        ease-in-out;}.overlay.active{display: block; opacity: 1;}#sidebar .sidebar-header{padding: 20px; background: 
        #6d7fcc;}#sidebar ul.components{padding: 20px 0; border-bottom: 1px solid #47748b;}#sidebar ul p{color: #fff; 
        padding: 10px;}#sidebar ul li a{padding: 10px; font-size: 1.1em; display: block;}#sidebar ul li a:hover{
        color: #7386D5; background: #fff;}#sidebar ul li.active>a,a[aria-expanded="true"]{color: #fff; background: 
        #6d7fcc;}a[data-toggle="collapse"]{position: relative;}.dropdown-toggle::after{display: block; position: 
        absolute; top: 50%; right: 20px; transform: translateY(-50%);}ul ul a{font-size: 0.9em !important; 
        padding-left: 30px !important; background: #6d7fcc;}ul.CTAs{padding: 20px;}ul.CTAs a{text-align: center; 
        font-size: 0.9em !important; display: block; border-radius: 5px; margin-bottom: 5px;}a.download{background: 
        #fff; color: #7386D5;}a.article,a.article:hover{background: #6d7fcc !important; color: #fff !important;}/* 
        --------------------------------------------------- CONTENT 
        STYLE----------------------------------------------------- */#content{width: 100%; padding: 20px; min-height: 
        100vh; transition: all 0.3s; position: absolute; top: 0; right: 0;}</style> <link rel="stylesheet" 
        href="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css" 
        integrity="sha384-9gVQ4dYFwwWSjIDZnLEWnxCjeSWFphJiwGPXr1jddIhOegiu1FwO5qRGvFXOdJZ4" 
        crossorigin="anonymous"><!-- Our Custom CSS <link rel="stylesheet" href="style5.css"> --> <script defer 
        src="https://use.fontawesome.com/releases/v5.0.13/js/solid.js" 
        integrity="sha384-tzzSw1/Vo+0N5UhStP3bvwWPq+uvzCMfrN1fEFe+xBmv1C/AtVX5K0uZtmcHitFZ" 
        crossorigin="anonymous"></script> <script defer 
        src="https://use.fontawesome.com/releases/v5.0.13/js/fontawesome.js" 
        integrity="sha384-6OIrr52G08NpOFSZdxxz1xdNSndlD4vdcf/q2myIUVO0VsqaGHJsB0RaBE01VTOY" 
        crossorigin="anonymous"></script> <script type="text/javascript"></script></head> <body> <div 
        class="wrapper"> <nav id="sidebar" style="min-width: 250px; max-width:250px"> <div id="dismiss"> <i 
        class="fas fa-arrow-left"></i> </div><div class="sidebar-header"> <h4>SecurusAudire</h4> </div><ul 
        class="list-unstyled components"> <li> <a class="link" href="#" id="Warnings" style="text-decoration:none; 
        color: white;">Warnings</a> </li> <li> <a class="link" href="#" id="Suggestions" style="text-decoration:none; 
        color: white;">Suggestions</a> </li> <li> <a class="link" href="#AuditSubmenu" style="text-decoration:none; 
        color: white;" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle" id="Audit">Audit</a> <ul 
        class="collapse list-unstyled" id="AuditSubmenu"> """

    def generate_side_nav_bar(self):
        """
        Format - 
                <li>
                    <a class="link" href="#homeSubmenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle" id="home">Home</a>
                    <ul class="collapse list-unstyled" id="homeSubmenu">
                        <li>
                            <a class="link" href="#" id="home_1">Home 1</a>
                        </li>
                        <li>
                            <a class="link" href="#" id="home_2">Home 2</a>
                        </li>
                        <li>
                            <a class="link" href="#" id="home_3">Home 3</a>
                        </li>
                    </ul>
                </li>
        """
        list_item = ""

        for module_name in self.audit_result.keys():
            sub_list = ""
            for test_name in self.audit_result[module_name].keys():
                temp_sub_list = f"""
                    <li>
                    <a class="link" style="text-decoration:none; color: white;" href="#" id="{module_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}_{test_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}">{test_name}</a>
                    </li>
                """
                sub_list += temp_sub_list

            temp_main_list = f"""
                <li>
                <a class="link" style="text-decoration:none; color: white;" href="#{module_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}SubMenu" data-toggle="collapse" aria-expanded="false" class="dropdown-toggle" id="{module_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}">{module_name}</a>
                <ul class="collapse list-unstyled" id="{module_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}SubMenu">{sub_list}
                </li>
            """

            list_item += temp_main_list

        list_item += '</ul></li></ul></nav>'

        return list_item

    def get_html_table_from_dict(self, dict_to_convert: dict):

        # converting dictionary to json
        json_data = self.util_obj.convert_dict_to_json(dict_convert=dict_to_convert)

        # converting json to html table
        converted_table = self.util_obj.convert_json_to_html_table(json_data=json_data)

        return converted_table

    def generate_main_content(self):

        complete_table = self.get_html_table_from_dict(self.full_report)
        main_table = self.get_html_table_from_dict(self.audit_result)

        system_score = self.full_report["System Score"]
        total_score_possible = self.full_report["Total Score Possible"]
        audit_start_time = self.full_report["Audit Start Time"]
        audit_end_time = self.full_report["Audit End Time"]
        audit_duration = self.full_report["Audit Duration"]
        try:
            hardening_index = round((system_score / total_score_possible) * 100, 2)
        except ZeroDivisionError:
            hardening_index = 0.00

        main_content = f""" <div id="content"> <nav class="navbar navbar-expand-lg navbar-light bg-light"> <div class="container-fluid"> <button type="button" id="sidebarCollapse" class="btn btn-info"> <i class="fas fa-align-left"></i> <span></span> </button> <button class="btn btn-dark d-inline-block d-lg-none ml-auto" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation"> <i class="fas fa-align-justify"></i> </button> <div class="collapse navbar-collapse" id="navbarSupportedContent"> <ul class="nav navbar-nav ml-auto"> <li class="nav-item active"> <h4>Web Report</h4> </li></ul> </div></div></nav><!--Score--><hr /><div id="score" class="row"><div class="col"><h5 style="margin: auto; text-align: center;">Total Score - {system_score}/{total_score_possible}</h5></div><div class="col"><h5 style="margin: auto; text-align: center;"> Hardening Index - {hardening_index}%</h5></div></div><hr /><div id="time" class="row"><div class="col"><h5 style="margin: auto; text-align: center;">Audit Start Time - {audit_start_time}</h5></div><div class="col"><h5 style="margin: auto; text-align: center;"> Audit End Time - {audit_end_time}</h5></div></div><hr /><div id="duration" class="row"><div class="col"><h5 style="margin: auto; text-align: center;"> Audit Duration - {audit_duration}</h5></div></div> 
        <hr /><br /><hr /><div id="main_table"><h5>Full Report</h5><hr /><br />{complete_table}</div><div id="main_content"><div id="Audit_content"><a class="go_back" href="#main_table"><h5>Full Report</a> > Audit Results</h5><hr /><br />{main_table}</div>"""

        for module_name in self.audit_result.keys():
            sub_table = self.get_html_table_from_dict(self.audit_result[module_name])
            temp_sub_content = f"""
                <div id="{module_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}_content"><a class="go_back" href="#main_table"><h5>Full Report</a> > {module_name}</h5><hr /><br />{sub_table}</div>
            """
            main_content += temp_sub_content

            for test_name in self.audit_result[module_name].keys():
                test_table = self.get_html_table_from_dict(self.audit_result[module_name][test_name])

                temp_test_content = f"""
                <div id="{module_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}_{test_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}_content"><a class="go_back" href="#main_table"><h5>Full Report</a> > <a class="go_back" href="#{module_name.replace(' ', '').replace('.', '').replace('(', '').replace(')', '')}_content">{module_name}</a> > {test_name}</h5><hr /><br />{test_table}</div> 
            """
                main_content += temp_test_content

        # adding warning table
        warnings_table = self.get_html_table_from_dict(self.full_report["Warnings"])
        main_content += f'<div id="Warnings_content"><a class="go_back" href="#main_table"><h5>Full Report</a> > ' \
                        f'Warnings</h5><hr /><br />{warnings_table}</div> '

        # adding suggestion table
        suggestions_table = self.get_html_table_from_dict(self.full_report["Suggestions"])
        main_content += f'<div id="Suggestions_content"><a class="go_back" href="#main_table"><h5>Full Report</a> > ' \
                        f'Suggestions</h5><hr /><br />{suggestions_table}</div> '

        main_content += '</div></div></div>'

        return main_content

    def parse_result(self):
        side_nav_bar = self.generate_side_nav_bar()
        self.file_content += side_nav_bar
        main_content = self.generate_main_content()
        self.file_content += main_content
        self.file_content += """<div class="overlay"></div> <script 
        src="https://code.jquery.com/jquery-3.3.1.slim.min.js" 
        integrity="sha384-q8i/X+965DzO0rT7abK41JStQIAqVgRVzpbzo5smXKp4YfRvH+8abtTE1Pi6jizo" 
        crossorigin="anonymous"></script> <script 
        src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.0/umd/popper.min.js" 
        integrity="sha384-cs/chFZiN24E4KMATLdqdvsezGxaGsi4hLGOzlXwp5UZB1LY//20VyM2taTB4QvJ" 
        crossorigin="anonymous"></script> <script 
        src="https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/js/bootstrap.min.js" 
        integrity="sha384-uefMccjFJAIv6A+rW+L4AHf99KvxDjWSu1z9VI8SKNVmz4sk7buKt/6v9KI65qnm" 
        crossorigin="anonymous"></script> <script 
        src="https://cdnjs.cloudflare.com/ajax/libs/malihu-custom-scrollbar-plugin/3.1.5/jquery.mCustomScrollbar
        .concat.min.js"></script> <script type="text/javascript">$(document).ready(function (){$(
        "#sidebar").mCustomScrollbar({theme: "minimal"}); $('#dismiss, .overlay').on('click', function (){$(
        '#sidebar').removeClass('active'); $('.overlay').removeClass('active');}); $('#sidebarCollapse').on('click', 
        function (){$('#sidebar').addClass('active'); $('.overlay').addClass('active'); $(
        '.collapse.in').toggleClass('in'); $('a[aria-expanded=true]').attr('aria-expanded', 'false');}); $(
        "#main_content div").hide(); $(".link").click(function(){$("#main_content div").hide(); $(
        "#main_table").hide(); $("#"+$(this).attr("id")+"_content").show();});}); $(".go_back").click(function(){$(
        "#main_content div").hide(); $("#main_table").hide(); $($(this).attr("href")).show();});</script> 
        </body></html> """

        self.create_file(self.file_content)

    def create_file(self, file_content):

        if CURR_SYSTEM_PLATFORM == "windows":
            if not self.util_obj.check_file_exsists(self.save_folder_location + r"\SecurusAudire_Reports"):
                makedirs(self.save_folder_location + r'\SecurusAudire_Reports')

            complete_location = rf"{self.save_folder_location}\SecurusAudire_Reports\web_report-{self.timestamp}.html"

        else:
            if not self.util_obj.check_file_exsists(self.save_folder_location + r"/SecurusAudire_Reports"):
                makedirs(self.save_folder_location + r'/SecurusAudire_Reports')

            complete_location = f"{self.save_folder_location}/SecurusAudire_Reports/web_report-{self.timestamp}.html"

        with open(complete_location, 'w+') as write_file_obj:
            write_file_obj.write(self.file_content)

    def generate_report(self):
        self.parse_result()
