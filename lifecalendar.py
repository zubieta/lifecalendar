#!/usr/bin/env python
# -*- encoding: UTF-8 -*-
"""Tool to create an image of the life calendar, where each square
represents a week in our life."""
from argparse import ArgumentParser, RawDescriptionHelpFormatter, FileType
from configparser import ConfigParser
from datetime import datetime, date
from random import randint
from operator import add
from sys import stderr
from PIL import Image, ImageDraw, ImageFont


DEFAULT_CONFIG = {
        'image_size': '1366x768',
        'rectangle_size': '5x5',
        'life_expectancy': '80',
        'background': '#030508',
        'foreground': '#2A2A2A',
        'rectangle_colors':'#343434,#2E643D,#589F43,#98BC21,#B9FC04',
        'font_size': '12',
        'font_index': '0',
        'font_encoding': 'unic',
        'output_file': 'lifecalendar.png'
        }


def life_calendar():
    try:
        # Cli options
        epilog = """
Inspired by the TED Talk: "Inside the mind of a master procrastinator"
by Tim Urban.
https://www.ted.com/talks/tim_urban_inside_the_mind_of_a_master_procrastinator
"""
        parser = ArgumentParser(description=__doc__, epilog=epilog,
                                formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument('-c', '--config', type=FileType('r'),
                            help='configuration file.')

        group = parser.add_argument_group('Configuration overriders',
                description='If set they take precedence over the values '
                            'especified in the configuration.')
        group.add_argument('-o', '--output', help='output file.')
        group.add_argument('-b', '--birthdate',
                            help='birthdate in the format "dd/mm/yyyy."')
        group.add_argument('-y', '--life-expectancy',
                            help='life expectancy in years.')

        args = parser.parse_args()

        # Parse configuration file
        parser = ConfigParser(interpolation=None)
        parser['DEFAULT'] = DEFAULT_CONFIG
        if args.config:
            parser.read_string('[config]\n' + args.config.read())
            config = dict(parser.items('config'))
        else:
            config = DEFAULT_CONFIG

        # Merge cli and config settigns
        if args.output:
            config['output_file'] = args.output
        if args.birthdate:
            config['birthdate'] = args.birthdate
        if args.life_expectancy:
            config['life_expectancy'] = args.life_expectancy

        # Text default color = foreground
        if not config.get('font_color'):
            config['font_color'] = config['foreground']

        # return a tuple of integers from a string with `x` as separator
        xplit = lambda string: tuple(int(x) for x in string.split('x'))
        # Parse config strings
        config['image_size'] = xplit(config['image_size'])
        config['rectangle_size'] = xplit(config['rectangle_size'])
        config['life_expectancy'] = int(config['life_expectancy'])
        config['rectangle_colors'] = config['rectangle_colors'].split(',')
        config['font_size'] = int(config['font_size'])
        config['font_index'] = int(config['font_index'])
        try:
            config['birthdate'] = datetime.strptime(config['birthdate'],
                                                    '%d/%m/%Y')
        except KeyError:
            print('Error: Missing birthdate value', file=stderr)
            exit(1)
        except ValueError as err:
            print('Error: {}'.format(err), file=stderr)
            exit(1)

        if not config.get('output_file'):
            print('Error: Missing output_file value', file=stderr)
            exit(1)

        # Time
        diff_weeks = lambda start, end: ((end - start).days + 1) // 7
        lived_weeks = diff_weeks(config['birthdate'], datetime.now())
        weeks_in_life = diff_weeks(config['birthdate'],
                datetime(config['birthdate'].year + config['life_expectancy'],
                         config['birthdate'].month,
                         config['birthdate'].day))


        rand_index = lambda : randint(0, len(config['rectangle_colors']) - 1)
        color = (lambda week: (config['rectangle_colors'][rand_index()],) * 2
                              if week < lived_weeks
                              else (config['background'], config['foreground']))


        # Tuple pair wise sum
        pws = lambda x, y: tuple(map(add, x, y))

        # Geometry
        grid = ((weeks_in_life + 51) // 52, 52)
        grid_offset = tuple(map(lambda s, r, g: (s - r * (g * 2 - 1)) // 2,
                                config['image_size'], config['rectangle_size'],
                                grid))
        offset = lambda week: pws((2 * config['rectangle_size'][0] * (week//52),
                                   2 * config['rectangle_size'][1] * (week%52)),
                                   grid_offset)
        corners = lambda week: (offset(week),
                                pws(offset(week), config['rectangle_size']))
        text_offset = pws((-config['rectangle_size'][0], 0 ),
                          map(lambda r, g, o: 2 * r * g + o,
                              config['rectangle_size'],
                              grid, grid_offset))

        # Text
        if config.get('font'):
            # PIL font
            if config['font'].strip().split('.')[-1].lower() == 'pil':
                font = ImageFont.load_path(config['font'])
            else:
                font = ImageFont.truetype(config['font'],
                                          size=config['font_size'],
                                          index=config['font_index'],
                                          encoding=config['font_encoding'])
        else:
            font = ImageFont.load_default()
        lived_msg = '{} weeks lived'.format(lived_weeks)
        left_msg = 'approx. {} weeks left'.format(weeks_in_life - lived_weeks)

        # Image
        image = Image.new('RGBA', config['image_size'], config['background'])
        drawer = ImageDraw.Draw(image)
        for week in range(grid[0] * grid[1]):
            drawer.rectangle(corners(week), *color(week))
        drawer.text((grid_offset[0], text_offset[1]), lived_msg, font=font,
                    fill=config['font_color'])
        drawer.text((text_offset[0] - font.getsize(left_msg)[0], text_offset[1]),
                    left_msg, font=font, fill=config['font_color'])
        try:
            image.save(config['output_file'])
        except KeyError as err:
            fmt = config['output_file'].split('.')[-1]
            raise ValueError('Image format not supported: {}'.format(fmt))
    except Exception as err:
        print('Error: {}'.format(err), file=stderr)
        exit(1)


if __name__ == '__main__':
    life_calendar()
