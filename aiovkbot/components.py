import json

class Keyboard:
    """

    Example:
	Create keyboard with one row and append one button in frirst row:
        >>> keyboard = Keyboard(1); keyboard[0].append(CommandBtn('start', 'Start!')); print(keyboard)
        {"one_time": false, "inline": false, "buttons": [[{"color": "secondary", "action": {"type": "text", "label": "Start!", "payload": "{\\"command\\": \\"start\\"}"}}]]}
    """

    def __init__(self, len=None, inline=False, one_time=False, rows=None):
        self.__inline = inline
        self.__one_time = one_time
        self.__rows = rows or [[] for _ in range(len or 0)]

    def __len__(self):
        return len(self.__rows)

    @property
    def inline(self):
        return self.__inline

    @property
    def rows(self):
        return self.__rows

    def add_row(self, row=None):
        self.__rows.append(row or [])

    def __getitem__(self, val):
        return self.__rows[val]

    @property
    def T(self):
        """Transpose keyboard."""
        raise NotImplementedError
    @property
    def json(self):
        return {
            "one_time": self.__one_time,
            "inline": self.__inline,
            "buttons": [[btn.json for btn in row] for row in self.__rows]
        }

    def __str__(self):
        return json.dumps(self.json)

    def __add__(self, keyboard):
        """merge keyboards"""
        if not keyboard:
            return self

        return Keyboard(
            rows=self.rows + keyboard.rows,
            inline=self.__inline,
            one_time=self.__one_time
        )

    __radd__ = __add__


class CommandBtn:
    """Text button with command in payload

    Example:
        >>> print(CommandBtn('help', 'Get help'))
	{"color": "secondary", "action": {"type": "text", "label": "Get help", "payload": "{\\"command\\": \\"help\\"}"}}
    """

    SECONDARY = 'secondary'
    PRIMARY = 'primary'
    POSITIVE = 'positive'
    NEGATIVE = 'negative'
    AVAILABLE_COLORS = {SECONDARY, PRIMARY, POSITIVE, NEGATIVE}

    def __init__(self, command, label, data=None, color=None):
        self.__payload = {"command": command}
        self.__payload.update(data or dict())
        self.__label = label
        self.__color = color if color in self.AVAILABLE_COLORS else self.SECONDARY

    @property
    def json(self):
        return {
            "color": self.__color,
            "action":{
                "type": 'text',
                "label": self.__label,
                "payload": json.dumps(self.__payload)
            }
        }

    def __str__(self):
        return json.dumps(self.json)

class LinkBtn:
    """Open link button
    Example:
        >>> print(LinkBtn('http://', 'Redirect'))
	{"action": {"type": "openlink", "link": "http://", "label": "Redirect"}}
	"""

    def __init__(self, link, label):
        self.__link = link
        self.__label = label

    @property
    def json(self):
        return {
            "action":{
                "type": 'openlink',
                "link": self.__link,
                "label": self.__label,

            }
        }
    def __str__(self):
        return json.dumps(self.json)

if __name__ == "__main__":
    from doctest import testmod; testmod()

