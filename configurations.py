class Load_Configuation:
    # 
    vars={
        "port":["str"],
        "genesis_hash":["str"]
        "node_ip":["str"]
        "version":["str"]
        "whitelist":["list"]
        "blacklist"["list"]
        "show_address":["str"]
        "accept_peers":["str"]
    }

    def read_default(self):
        # Load default configuration
        
