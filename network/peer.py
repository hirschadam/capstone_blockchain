class Peer(object):

	def __init__(self, idx, name, ip_addr, port_recv):

		"""
		Constructor for Peer
		@param idx - peer identifier
		@param name - peer name
		@param ip_addr - peer ip address
		@param port_recv - receving port
		"""
		self.idx = idx
		self.name = name
		self.ip_addr = ip_addr
		self.port_recv = port_recv
