from queue import Queue

class LexicalAnalyzer:
    def __init__(self, program_filename, batch_size=1024):
        self.ch = ''
        self.buf = ''
        self.state = ['H', 'ID', 'NUM', 'COM', 'ASGN', 'DLM', 'FIN', 'ER', 'COMM', 'ERCOM']
        self.TW = [  
            'True', 'False', 'null', 'and', 'or', 'not', 'in', 'do', 'else', 'condition',
            'break', 'continue', 'switch', 'case', 'default', 'loop', 'function', 'class',
            'return', 'try', 'except', 'interrupt'
        ]
        self.TD = ['(', ')', ',', ':', ':=', ';', '=', '{', '}', '[', ']', '+', '-',
                   '<', '>', '!', '&', '|', '/*', '*/', '/', '*']
        self.TNUM = []
        self.TID = []
        self.dt = 0
        self.current_state = 'H'
        self.program_filename = program_filename
        self.batch_size = batch_size
        self.code_queue = Queue()
        self.lexeme_list = []
        self.status = ''

    def enqueue_batches(self):
        """Read the file in chunks and enqueue each batch into the queue."""
        with open(self.program_filename, 'r') as file:
            while True:
                batch = file.read(self.batch_size)
                if not batch:
                    break
                self.code_queue.put(batch)

    def get_next(self):
        """Get the next character from the queue."""
        if self.chunks and len(self.chunks) > self.chunk_index:
            self.ch = self.chunks[self.chunk_index]
            self.chunk_index += 1
        else:
            self.chunks = self.code_queue.get() if not self.code_queue.empty() else ''
            self.chunk_index = 0
            self.ch = self.chunks[self.chunk_index] if self.chunks else ''

    def clear(self):
        self.buf = ''

    def add(self):
        self.buf += self.ch

    def look(self, cls):
        if self.buf in cls:
            return cls.index(self.buf)
        else:
            return -1

    def put(self, cls):
        if self.buf not in cls:
            cls.append(self.buf)
        return cls.index(self.buf)

    def putnum(self, cls):
        if self.dt not in cls:
            cls.append(self.dt)
        return cls.index(self.dt)

    def make_lex(self, cls, num):
        self.lexeme_list.append([cls, num])

    def run_analysis(self):
        self.enqueue_batches()  
        self.chunks = ''
        self.chunk_index = 0
        self.get_next()  

        while True:
            if self.current_state == 'H':
                if self.ch in [' ', '\n', '\t']:
                    self.get_next()
                elif self.ch.isalpha():
                    self.clear()
                    self.add()
                    self.get_next()
                    self.current_state = 'ID'
                elif self.ch.isdigit():
                    self.dt = int(self.ch)
                    self.get_next()
                    self.current_state = 'NUM'
                elif self.ch == '/':
                    self.get_next()
                    if self.ch == '*':
                        self.current_state = 'COM'
                elif self.ch == ':':
                    self.get_next()
                    self.current_state = 'ASGN'
                elif self.ch == '}':
                    self.make_lex(2, 8)
                    self.current_state = 'FIN'
                else:
                    self.current_state = 'DLM'

            elif self.current_state == 'ID':
                if self.ch.isalpha() or self.ch.isdigit():
                    self.add()
                    self.get_next()
                else:
                    j = self.look(self.TW)
                    if j != -1:
                        self.make_lex(1, j)
                    else:
                        j = self.put(self.TID)
                        self.make_lex(4, j)
                    self.current_state = 'H'

            elif self.current_state == 'NUM':
                if self.ch.isdigit():
                    self.dt = self.dt * 10 + int(self.ch)
                    self.get_next()
                else:
                    j = self.putnum(self.TNUM)
                    self.make_lex(3, j)
                    self.current_state = 'H'

            elif self.current_state == 'COM':
                while self.current_state == 'COM':
                    self.get_next()
                    if self.ch == '*':
                        self.get_next()
                        if self.ch == '/':
                            self.current_state = 'H'
                        elif self.ch == '\n':
                            self.current_state = 'ERCOM'

            elif self.current_state == 'DLM':
                self.clear()
                self.add()
                j = self.look(self.TD)
                if j != -1:
                    self.get_next()
                    self.make_lex(2, j)
                    self.current_state = 'H'
                else:
                    self.current_state = 'ER'

            elif self.current_state == 'ASGN':
                if self.ch == '=':
                    self.make_lex(2, 4)
                else:
                    self.make_lex(2, 3)
                self.get_next()
                self.current_state = 'H'

            if self.current_state in ['FIN', 'ER', 'ERCOM']:
                break

        if self.current_state == 'ER':
            self.status = 'LEXICAL | ERROR: Please check program for errors!'
        elif self.current_state == 'ERCOM':
            self.status = 'LEXICAL | ERROR: Please check comments!'
        elif self.current_state == 'FIN':
            self.status = 'LEXICAL | Analysis completed successfully!'

        return self.lexeme_list
