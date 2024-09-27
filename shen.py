# MIT License
#
# Copyright (c) 2022-2024 Ferhat Geçdoğan All Rights Reserved.
# Distributed under the terms of the MIT License.
#
# shen - syntax highlighter thing
# -------------------------------
# simplest way to highlighting your code as fast and simple as possible.
#
# github.com/ferhatgec/shen
#
# note: it's really bad written code but since it works (battle-tested for sure), i don't care; but prs are welcome!

from re import search
from html import escape

class shen_syntax_rule:
  class shen_color:
    def __init__(self, r, g, b, pattern, ends_with='', enable_regex=False, current_char_coloring=True):
      self.r = r
      self.g = g
      self.b = b

      self.pattern: str = pattern
      self.ends_with: str = ends_with
      self.enable_regex = enable_regex
      self.include_current_char_coloring = current_char_coloring

    def return_inside(self):
      return self

  def __init__(self):
    self.supported_tokens = dict()
    self.push_tokens = []
    self.capture_through = dict()
    self.ignored_tokens = []


class shen:
  @staticmethod
  def __escape_extra(data: str) -> str:
    return escape(data).replace(' ', '&nbsp;').replace('\n', '<br>\n') # last \n added for readability

  def __init__(self):
    self.tokens = []
    self.current_token: str = ''
    self.__collect = False
    self.__capture_ch = ''

  def highlight(self, data: str, syntax_rule: shen_syntax_rule, get_as_html: bool = False) -> [str]:
    if len(syntax_rule.push_tokens) == 0:
      return ['push_token[] is empty']

    for ch in data:
      if (syntax_rule.capture_through.get(ch) is not None) or self.__collect:
        if self.__collect:
          if ch == self.__capture_ch or (ch == syntax_rule.capture_through.get(self.__capture_ch).ends_with):
            if len(self.current_token) > 0:
              self.current_token += ch
              data = syntax_rule.capture_through.get(self.__capture_ch)

              if data.enable_regex:
                val = search(data.pattern, self.current_token)

                if val is not None:
                  val_data = val.groups()
                  if len(val_data) >= 1:
                    if ch == syntax_rule.capture_through.get(self.__capture_ch).ends_with:
                      if data.include_current_char_coloring:
                        self.tokens.append(
                          f'<span style=\"color: rgb({data.r}, {data.g}, {data.b})\">{shen.__escape_extra(self.__capture_ch)}{val_data[0]}{shen.__escape_extra(ch)}</span>'
                          if get_as_html
                          else f'\x1b[38;2;{data.r};{data.g};{data.b}m{self.__capture_ch}{val_data[0]}{ch}\x1b[0m'
                        )
                      else:
                        self.tokens.append(
                          f'{shen.__escape_extra(self.__capture_ch)}<span style=\"color: rgb({data.r}, {data.g}, {data.b})\">{val_data[0]}</span>{shen.__escape_extra(ch)}'
                          if get_as_html
                          else f'{self.__capture_ch}\x1b[38;2;{data.r};{data.g};{data.b}m{val_data[0]}\x1b[0m{ch}'
                        )
                    else:
                      if data.include_current_char_coloring:
                        self.tokens.append(
                          f'<span style=\"color: rgb({data.r}, {data.g}, {data.b})\">{shen.__escape_extra(ch)}{val_data[0]}{shen.__escape_extra(ch)}</span>'
                          if get_as_html
                          else f'\x1b[38;2;{data.r};{data.g};{data.b}m{ch}{val_data[0]}{ch}\x1b[0m'
                        )
                      else:
                        self.tokens.append(
                          f'{shen.__escape_extra(ch)}<span style=\"color: rgb({data.r}, {data.g}, {data.b})\">{val_data[0]}</span>{shen.__escape_extra(ch)}'
                          if get_as_html
                          else f'{ch}\x1b[38;2;{data.r};{data.g};{data.b}m{val_data[0]}\x1b[0m{ch}'
                        )
                else:
                  self.__collect = False
                  self.current_token += ch
                  continue
              else:
                self.tokens.append(self.current_token)

              self.current_token = ''
              self.__collect = False
          else:
            self.current_token += ch
        else:
          self.__collect = True
          self.__capture_ch = ch
          self.current_token += ch

        continue

      match ch:
        case ch if (ch in syntax_rule.push_tokens) or (self.current_token in syntax_rule.push_tokens):
          if len(self.current_token) > 0:
            data = syntax_rule.supported_tokens.get(self.current_token)

            if data is not None:
              if data.enable_regex:
                val = search(data.pattern, self.current_token).groups()

                if len(val) >= 1:
                  self.tokens.append(
                    f'<span style=\"color: rgb({data.r}, {data.g}, {data.b})\">{val[1]}</span>'
                    if get_as_html
                    else f'\x1b[38;2;{data.r};{data.g};{data.b}m{val[1]}\x1b[0m'
                  )
              else:
                self.tokens.append(
                  f'<span style=\"color: rgb({data.r}, {data.g}, {data.b})\">{self.current_token}</span>'
                  if get_as_html
                  else f'\x1b[38;2;{data.r};{data.g};{data.b}m{self.current_token}\x1b[0m'
                )
            else:
              self.tokens.append(self.current_token)

          self.current_token = ''

          if ch not in syntax_rule.ignored_tokens and not self.__collect:
            data = syntax_rule.supported_tokens.get(ch)

            if data is not None:
              self.tokens.append(
                f'<span style=\"color: rgb({data.r}, {data.g}, {data.b})\">{shen.__escape_extra(ch)}</span>'
                if get_as_html
                else f'\x1b[38;2;{data.r};{data.g};{data.b}m{ch}\x1b[0m'
              )
            else:
              self.tokens.append(shen.__escape_extra(ch) if get_as_html else ch)

          continue

        case _:
          self.current_token += shen.__escape_extra(ch) if get_as_html else ch

    return self.tokens
