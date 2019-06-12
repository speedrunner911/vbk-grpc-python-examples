

import grpc
import binascii

import veriblock_pb2
import veriblock_pb2_grpc

import base64
import base58

channel = grpc.insecure_channel('localhost:10502')
client = veriblock_pb2_grpc.AdminStub(channel)


# utils
def convertAtomicToVbkUnits(input):
	return input/100000000


def convertAddressToByteString(address):
	test = base64.b16encode(address)
	lolbytes = base58.b58encode(test)
	return lolbytes



def getInfo():
	res = client.GetInfo(veriblock_pb2.GetInfoRequest())
	if not res:
		print("Error")
	print("NC_CLI command: getinfo")
	print("LastBlock.Hash="+ binascii.hexlify(res.last_block.hash))
	print("EstimatedHasrate=" + str(res.estimated_hashrate) + "h/s")


def getStateInfo():
	res = client.GetStateInfo(veriblock_pb2.GetStateInfoRequest())
	if not res:
		print("Error")
	print("NC_CLI command: getstateinfo")
	print("NetworkVersion=" +res.network_version)
	print("LocalBlockchainHeight="+str(res.local_blockchain_height))


def getBlockByIndex():
	filters = veriblock_pb2.BlockFilter(index=100)
	res = client.GetBlocks(veriblock_pb2.GetBlocksRequest(search_length=2000, filters=[filters]))
	if len(res.blocks) > 0:
		# display info
		print("GetBlockByIndex")
		print("NC_CLI command: getblockfromindex <blockIndex>")
		blockHash = binascii.hexlify(res.blocks[0].hash)
		print("BlockHash= " + blockHash)
		

def getTranasctionById():
	txId = "12498E1EF73BCA555C5EB1F0AC1D7C6D8F3256DEED9AE7A78C74DD7A762D1B8B"
	test = base64.b16decode(txId)

	res = client.GetTransactions(veriblock_pb2.GetTransactionsRequest(search_length=2000, ids=[test]))
	if len(res.transactions) > 0:
		print("GetTransactionById");
		print("NC_CLI command: gettransaction <txId> [searchLength]");


		blockIndex = res.transactions[0].block_number
		amount = convertAtomicToVbkUnits(res.transactions[0].transaction.source_amount)
		print("BlockIndex=" + str(blockIndex) + " SourseAmount=" + str(amount))



def getBalance():
	address = "VFXWGNLcGR4vTCSU6VAMXvgru9EKk3"

	bytesAddress = base58.b58decode(address)

	res = client.GetBalance(veriblock_pb2.GetBalanceRequest(addresses=[bytesAddress]))
	if res.success:
		print("GetBalance")
		print("NC_CLI commad: getbalance [address]")
		confirmed = str(convertAtomicToVbkUnits(res.confirmed[0].unlocked_amount)) + " VBK"
		pending = str(convertAtomicToVbkUnits(res.unconfirmed[0].amount)) + " VBK"
		print("Confirmed= " + confirmed)
		print("Pending= " + pending)
	


def getNewAddress():
	# generate address
	res = client.GetNewAddress(veriblock_pb2.GetNewAddressRequest(count=2))
	if res.success: 
		print("GetNewAddress")
		print("NC_CLI command: getnewaddress")

		address = base58.b58encode(res.address)
		print("New address: " + address)



def sendTransaction():
	sourseAddress = "VFXWGNLcGR4vTCSU6VAMXvgru9EKk3"
	targetAddress = "V5gb4UCrzn7rxzqaJE9EYNvZoF3KUC"
	amount = 10

	targetBytesAddress = base58.b58decode(targetAddress)
	sourseBytesAddress = base58.b58decode(sourseAddress)
	
	output = veriblock_pb2.Output(address=targetBytesAddress, amount=amount)

	# Note - could create multiple Tx, pick just the first one for demo:
	res = client.SendCoins(veriblock_pb2.SendCoinsRequest(source_address=sourseBytesAddress, amounts=[output] ))
	if res.success:
		print("SendTransaction")
		print("NC_CLI command: send <amount> <destinationAddress> [sourceAddress]")

		txHash = binascii.hexlify(res.tx_ids[0])
		print("Created transaction: " + txHash)



def run():
	print("-------------- GetInfo --------------")
	getInfo()
	print("-------------- GetStateInfo --------------")
	getStateInfo()
	print("-------------- GetBlockByIndex --------------")
	getBlockByIndex()
	print("-------------- GetTranasctionById --------------")
	getTranasctionById()
	print("-------------- GetNewAddress -------------------")
	getNewAddress()
	print("-------------- GetBalance ----------------------")
	getBalance()
	print("-------------- SendTransaction -----------------")
	sendTransaction()

run()


