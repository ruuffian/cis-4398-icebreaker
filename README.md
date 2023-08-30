# calexport

A simple Python script that automatically exports CIS 4398 assignments as an iCal file.


## Getting Started

### Dependencies

Python 3.8, pytz 2023.3, python-dotenv 

### Installing

Step 1: After cloning the repository, run `pip3 install -r requirements.txt` to install the project dependencies.<br />
Step 2: Inside .env.dev, replace YOUR_TOKEN_HERE with your ianapplebaum API token.<br />
Step 3: Rename .env.dev to .env<br /><br />
Now, you're ready to convert the CIS 4398 schedule into a .ics file!

### Executing program

Usage:
```
calexport file_name [-t <target_directory>]
```

## Help

```
calexport {-h|--help}
```

## Authors

Alan Uthuppan

Cynthia To

Liam Mackay

Andy Olshanky

Regina Oda


## License

This project is licensed under the MIT License - see the LICENSE.md file for details

## Acknowledgments

Inspiration, code snippets, etc.
* [README Template](https://github.com/matiassingers/awesome-readme)
* [argparse Documentation](https://docs.python.org/3/library/argparse.html)
