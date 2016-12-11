## LIFE CALENDAR

This is a small script that I wrote after watching the great TED Talk
[**"Inside the mind of a master procrastinator"**](https://www.ted.com/talks/tim_urban_inside_the_mind_of_a_master_procrastinator) by _Tim Urban_.

It's a customizable way to create a _life calendar_ image. Which can be
later used as the desktop background.

![Life calendar with the 'thought provoking' theme](https://github.com/zurwolf/lifecalendar/raw/master/examples/thought_provoking.png "Thought provoking theme example.")

## Dependencies

* python>=3.5
* Pillow==3.4.2

## Usage

    usage: lifecalendar.py [-h] [-c CONFIG] [-o OUTPUT] [-b BIRTHDATE]
                           [-y LIFE_EXPECTANCY]
    
    Tool to create an image of the life calendar, where each rectangle
    represents a week in our life.
    
    optional arguments:
      -h, --help            show this help message and exit
      -c CONFIG, --config CONFIG
                            configuration file.
    
    Configuration overriders:
      If set they take precedence over the values especified in the
      configuration.
    
      -o OUTPUT, --output OUTPUT
                            output file.
      -b BIRTHDATE, --birthdate BIRTHDATE
                            birthdate in the format "dd/mm/yyyy."
      -y LIFE_EXPECTANCY, --life-expectancy LIFE_EXPECTANCY
                            life expectancy in years.

## Examples

    python lifecalendar.py -c examples/default -b 14/03/1989 -y 85

For more examples of the configuration check the [examples folder](https://github.com/zurwolf/lifecalendar/tree/master/examples)

## LICENSE

It is licensed under the **GPLv3**. For the full license check the [LICENSE file](https://github.com/zurwolf/lifecalendar/blob/master/LICENSE).
