#!/usr/local/bin/lua
--Updated : 19/01/2024 
--Author: J Rivers
-- load the JSON library.
-- local Json = require("cjson")
local bit = require("bit32")
local CurrentIndex = 1
local DeviceRead = 1
local bytes11 = ""
local ByteArray = {0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0,0x0}
local XORArray = {0x41,0x21,0x73,0x55,0xa2,0xc1,0x32,0x71,0x66,0xaa,0x3b,0xd0,0xe2,0xa8,0x33,0x14,0x20,0x21,0xaa,0xbb}


--Decode Saved values
local D1eaBit = 0x00
local D1gcBit = 0x00
local DP2Flag = false
local D2eaBit = 0x00
local D2gcBit = 0x00
local DP3Flag = false
local D3eaBit = 0x00
local D3gcBit = 0x00
local DP4Flag = false
local D4eaBit = 0x00
local D4gcBit = 0x00


-- byte 4
local PeakFlag = false
local BUZFlag = false
local MinusFlag = false



-- byte 8
local HoldFlag = false
local FFlag = false
local CFlag = false
local DiodeFlag = false
--byte 9
local MaxFlag = false
local MinFlag = false
local PercentFlag = false
local ACFlag = false
local FaradFlag = false
local uFFlag = false
local mFFlag = false
local nFFlag = false
--byte 10
local HzFlag = false
local OhmFlag = false
local KiloOhmFlag = false
local MegaOhmFlag = false
local VoltFlag = false
local mVoltFlag = false
local DCFlag = false
local AmpFlag = false
-- byte 11
local AutoFlag = false
local uAmpFlag = false
local mAmpFlag = false

--Actual digits
local Digit1 = "0"
local Digit2 = "0"
local Digit3 = "0"
local Digit4 = "0"
-- Display Output String
local DispString = ""
local ReadSuccess = false
-- Used to determine if the device sending the string is DMM 11 Model (EN9002)bytes or Tong Current meter 10 Bytes Model(ST-207)
local DeviceType = 0
-- Used to capture all printed stiff and send to a file
function lprint(Msg)
	if Msg ~= nil then
		local pDateTime = os.date('%Y-%m-%d %H:%M:%S')
		print(Msg)
		local path = "/root/BTDMM.Log" --system.pathForFile( filename, "/root/")
		local file = io.open(path, "a+")
		if file then
			--print("File opened")
			file:write(pDateTime.." "..Msg.."\n")
			io.close( file )
		else
			print("Error File did not open")
		end
	else
		print("Log Message Empty")
	end
end
-- Used to Set the SSID and Key in the UCI interface for the new home network
RunCommands = function()
	
	os.execute("rm /tmp/Rheem/BTDMM.txt")
	--os.execute("gatttool -b  9C:0C:35:60:A1:1E --char-read --listen -a 9 |grep value: >/tmp/Rheem/BTDMM.txt &") -- DMM
	--os.execute("gatttool -b 9C:0C:35:56:35:DD --char-read --listen -a 9 |grep value: >/tmp/Rheem/BTDMM.txt &") -- Tong Curent tester
	
	os.execute("gatttool -b "..arg[CurrentIndex].." --char-read --listen -a 9 |grep value: >/tmp/Rheem/BTDMM.txt &") -- Tong Curent tester
	-- Looping through all devices assigned
	DeviceRead = CurrentIndex
	if CurrentIndex < #arg then
		CurrentIndex = CurrentIndex +1
	else
		CurrentIndex =1
	end
	os.execute("sleep 2") 
	os.execute("killall gatttool")
	--lprint("Commands run") 
end
-- Check if Wifi has connected
CheckResponse = function()
	local file = io.open( "/tmp/Rheem/BTDMM.txt", "r" )
	if file ~= nil then
		print("Device "..DeviceRead.." Response obtained")
		local Filecontents = file:read( "*a" )
		if Filecontents ~= nil then
			--print(Filecontents)
			--local Filecontents = file:lines()
			local indexstart = nil
			local indexend = nil
			indexstart, indexend = string.find(Filecontents,"value: ")
			indexstartE, indexendE = string.find(Filecontents,"\n")
			
			
			if indexstart ~= nil and indexend ~= nil then
				--print(indexstart.." "..indexend.." "..indexstartE.." "..indexendE)
				bytes11 = string.sub(Filecontents,indexend+1,indexstartE)
				DeviceType = 0
				local StLength = indexstartE - (indexend+1)
				
				--print(" StrLength "..StLength)
				if StLength == 33 then DeviceType = 11 end
				if StLength == 30 then DeviceType = 10 end
				--print("First "..bytes11)
				--bytes11 = "1b 84 70 b1 49 6a 9f 3c 66 aa 3b  " -- 11 Byte example
				--bytes11 = "1b 84 71 f1 2f 4e ad fe 6c aa " --10 byte example
				--print("Static "..bytes11)
			else
				lprint("Cannot decode response")
				bytes11 = "" 
				os.execute("hciconfig hci0 up piscan")
				--print("Recover hci0 device")
			end
			--Output = string.
			--print(bytes11)
		else
			bytes11 = "" 
			print("No response from device")
		end
	end
end
-- Check if Wifi has connected
DecodeBytes = function()
	--local DecodeStr = ""
	--print(bytes11)
	ReadSuccess = false
	local length = string.len(bytes11)
	local startbyte = 1
	local endbyte = 2
	local ByteIndex = 1
	--print("Str Len "..length)
	if string.len(bytes11) >= 30 then
		--print(bytes11)
		--print(DeviceType)
		for v=1,DeviceType,1 do
		
			local LocalStr = string.sub(bytes11,startbyte,endbyte)
			--print("two bytes "..LocalStr)
			local HexValue = tonumber(LocalStr,16)
			--print("Hex value "..HexValue)
			--print("Hexvalue "..HexValue)
			ByteArray[ByteIndex] = HexValue
			-- Perform XOR on the data
			ByteArray[ByteIndex] = bit.bxor(ByteArray[ByteIndex], XORArray[ByteIndex])
			--DecodeStr = DecodeStr.." "..string.format("%02x", ByteArray[ByteIndex])
			--print(" Byte "..ByteIndex.." value "..ByteArray[ByteIndex])
			startbyte = startbyte + 3
			endbyte = endbyte + 3
			ByteIndex = ByteIndex + 1
		end
		--print("Byte Array "..DecodeStr)
		ReadSuccess = true
	else
		--lprint("String not found")
		ReadSuccess = false
	end
end

-- Extract Bits from 11 Byte message
ProcessElements11 = function()
	--Decoding bits
	-- decode 7 segments
	-- byte 4, 5, 6, 7, 8
	DXeaBit = 0xE0
	DXgcBit = 0x0F
	DPBit = 0x10
	-- byte 4
	PeakBit = 0x02
	BUZBit = 0x08
	MinusBit = 0x10
	-- byte 8
	HoldBit = 0x10
	FBit = 0x20
	CBit = 0x40
	DiodeBit = 0x80
	--byte 9
	MaxBit = 0x01
	MinBit = 0x02
	PercentBit = 0x04
	ACBit = 0x08
	FaradBit = 0x10
	uFBit = 0x20
	mFBit = 0x40
	nFBit = 0x80
	--byte 10
	HzBit = 0x01
	OhmBit = 0x02
	KiloOhmBit = 0x04
	MegaOhmBit = 0x08
	VoltBit = 0x10
	mVoltBit = 0x20
	DCBit = 0x40
	AmpBit = 0x80
	-- byte 11
	AutoBit = 0x01
	uAmpBit = 0x04
	mAmpBit = 0x08
	--Decode Saved values
	D1eaBit = 0x00
	D1gcBit = 0x00
	DP2Flag = false
	D2eaBit = 0x00
	D2gcBit = 0x00
	DP3Flag = false
	D3eaBit = 0x00
	D3gcBit = 0x00
	DP4Flag = false
	D4eaBit = 0x00
	D4gcBit = 0x00


	-- byte 4
	PeakFlag = false
	BUZFlag = false
	MinusFlag = false
	-- byte 8
	HoldFlag = false
	FFlag = false
	CFlag = false
	DiodeFlag = false
	--byte 9
	MaxFlag = false
	MinFlag = false
	PercentFlag = false
	ACFlag = false
	FaradFlag = false
	uFFlag = false
	mFFlag = false
	nFFlag = false
	--byte 10
	HzFlag = false
	OhmFlag = false
	KiloOhmFlag = false
	MegaOhmFlag = false
	VoltFlag = false
	mVoltFlag = false
	DCFlag = false
	AmpFlag = false
	-- byte 11
	AutoFlag = false
	uAmpFlag = false
	mAmpFlag = false
	--Analys Byt 4
	local HexValue = ByteArray[4]
	--print("***Value byte 4 " ..HexValue)
	local BitValue = bit.band(HexValue, PeakBit)
	-- Check Peak Bit
	if BitValue >0 then
		PeakFlag = true
		--print("Peak on")
	end
	-- Check Buzzer Bit
	BitValue = bit.band(HexValue, BUZBit)
	if BitValue >0 then
		BUZFlag = true
		--print("Buzzer on")
	end
	-- Check Minus Bit
	BitValue = bit.band(HexValue, MinusBit)
	if BitValue >0 then
		MinusFlag = true
		--print("Minus on")
	end
	--Copy Ea 7 segment bits
	D1eaBit = bit.band(HexValue, DXeaBit)
	
	------------------------------------------------
	--Analys Byt 5
	local HexValue = ByteArray[5]
	--print("***Value byte 5 " ..HexValue)
	-- copy dc 7 segement bits
	D1gcBit = bit.band(HexValue, DXgcBit)
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, DPBit)
	if BitValue >0 then
			DP2Flag = true
		--print("Decimal point 2 on")
	end
	D2eaBit = bit.band(HexValue, DXeaBit)
	------------------------------------------------
	--Analys Byt 6
	local HexValue = ByteArray[6]
	--print("***Value byte 6 " ..HexValue)
	-- copy dc 7 segement bits
	D2gcBit = bit.band(HexValue, DXgcBit)
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, DPBit)
	if BitValue >0 then
			DP3Flag = true
		--print("Decimal point 3 on")
	end
	--Copy Ea 7 segment bits
	D3eaBit = bit.band(HexValue, DXeaBit)
	------------------------------------------------
	--Analys Byt 7
	local HexValue = ByteArray[7]
	--print("***Value byte 7 " ..HexValue)
	-- copy dc 7 segement bits
	D3gcBit = bit.band(HexValue, DXgcBit)
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, DPBit)
	if BitValue >0 then
		DP4Flag = true
		--print("Decimal point 4 on")
	end
	--Copy Ea 7 segment bits
	D4eaBit = bit.band(HexValue, DXeaBit)
	------------------------------------------------
	--Analys Byt 8
	local HexValue = ByteArray[8]
	--print("***Value byte 8 " ..HexValue)
	-- copy dc 7 segement bits
	D4gcBit = bit.band(HexValue, DXgcBit)
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, HoldBit)
	if BitValue >0 then
			HoldFlag = true
		--print("Hold on")
	end
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, FBit)
	if BitValue >0 then
			FFlag = true
		--print("F deg on")
	end
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, CBit)
	if BitValue >0 then
			CFlag = true
		--print("C degree on")
	end
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, DiodeBit)
	if BitValue >0 then
			DiodeFlag = true
		--print("Diode on")
	end
	------------------------------------------------
	--Analys Byt 9
	local HexValue = ByteArray[9]
	--print("***Value byte 9 " ..HexValue)
	BitValue = bit.band(HexValue, MaxBit)
	if BitValue >0 then
		MaxFlag = true
		--print("Max on")
	end
	BitValue = bit.band(HexValue, MinBit)
	if BitValue >0 then
		MinFlag = true
		--print("Min on")
	end
	BitValue = bit.band(HexValue, PercentBit)
	if BitValue >0 then
		PercentFlag = true
		--print("Percent on")
	end
	BitValue = bit.band(HexValue, ACBit)
	if BitValue >0 then
		ACFlag = true
		--print("AC on")
	end
	BitValue = bit.band(HexValue, FaradBit)
	if BitValue >0 then
		FaradFlag = true
		--print("Farad on")
	end
	BitValue = bit.band(HexValue, uFBit)
	if BitValue >0 then
		uFFlag = true
		--print("uF on")
	end
	BitValue = bit.band(HexValue, mFBit)
	if BitValue >0 then
		mFFlag = true
		--print("mF on")
	end
	BitValue = bit.band(HexValue, nFBit)
	if BitValue >0 then
		nFFlag = true
		--print("nF on")
	end
	------------------------------------------------
	--Analys Byt 10
	local HexValue = ByteArray[10]
	--print("***Value byte 10 " ..HexValue)
	BitValue = bit.band(HexValue, HzBit)
	if BitValue>0 then
		HzFlag = true
		--print("Hz on")
	end
	BitValue = bit.band(HexValue, OhmBit)
	if BitValue>0 then
		OhmFlag = true
		--print("Ohm on")
	end
	BitValue = bit.band(HexValue, KiloOhmBit)
	if BitValue>0 then
		KiloOhmFlag = true
		--print("Kilo Ohm on")
	end
	BitValue = bit.band(HexValue, MegaOhmBit)
	if BitValue>0 then
		MegaOhmFlag = true
		--print("MegaOhm on")
	end
	BitValue = bit.band(HexValue, VoltBit)
	if BitValue>0 then
		VoltFlag = true
		--print("Volt on")
	end
	BitValue = bit.band(HexValue, mVoltBit)
	if BitValue>0 then
		mVoltFlag = true
		--print("miliVolt on")
	end
	BitValue = bit.band(HexValue, DCBit)
	if BitValue>0 then
		DCFlag = true
		--print("DC on")
	end
	BitValue = bit.band(HexValue, AmpBit)
	if BitValue>0 then
		AmpFlag = true
		--print("Amp on")
	end
	--Analys Byt 11
	local HexValue = ByteArray[11]
    --print("***Value byte 11 " ..HexValue)
	BitValue = bit.band(HexValue, AutoBit)
	if BitValue>0 then
		AutoFlag = true
		--print("Auto on")
	end
	BitValue = bit.band(HexValue, uAmpBit)
	if BitValue>0 then
		uAmpFlag = true
		--print("uAmp on")
	end
	BitValue = bit.band(HexValue, mAmpBit)
	if BitValue>0 then
		mAmpFlag = true
		--print("milliAmp on")
	end
	
	--print("Value " ..HexValue)
	
	--print("AND Value " ..BitValue)
	--if bit.(HexValue,0x01)
end
-- Extract Bits from 11 Byte message
ProcessElements10 = function()
	local HexValue = 0
	local BitValue = 0
	--Decoding bits
	-- decode 7 segments
	-- byte 4, 5, 6, 7, 8
	local DXeaBit = 0xE0
	local DXgcBit = 0x0F
	local DPBit = 0x10
	-- byte 4
	local HoldBit = 0x02
	local BUZBit = 0x08
	local MinusBit = 0x10
	--byte 8
	local nanoBit = 0x10
	local VoltBit = 0x20
	local DCBit = 0x40
	--local DCBit = 0x40
	local ACBit = 0x80
	-- byte 9
	local FaradBit = 0x01
	local DiodeBit = 0x02
	local AmpBit = 0x04
	local microBit = 0x08
	local OhmBit = 0x10--0x01
	local B9Bit5 = 0x20
	local B9Bit6 = 0x40
	local MegaOhmBit = 0x80--0x08
	
	--local uFBit = 0x80
	--byte 10
	local B10Bit0 = 0x01
	local HzBit = 0x02--0x20
	local FBit = 0x04--0x40
	local CBit = 0x08
	local B10Bit4 = 0x10
	local KiloBit = 0x20--0x02
	local milliBit = 0x40--0x04
	local B10Bit7 = 0x80
	
	

	--Decode Saved values
	D1eaBit = 0x00
	D1gcBit = 0x00
	DP2Flag = false
	D2eaBit = 0x00
	DP3Flag = false
	D3eaBit = 0x00
	D3gcBit = 0x00
	DP4Flag = false
	D4eaBit = 0x00
	D4gcBit = 0x00


	-- byte 4
	HoldFlag = false	
	BUZFlag = false
	MinusFlag = false
	-- byte 8
	FaradFlag = false
	VoltFlag = false
	DCFlag = false
	-- byte 9
	nanoFlag = false
	DiodeFlag = false	
	AmpFlag = false
	microFlag = false
	OhmFlag = false
	B9Bit5Flag = false
	B9Bit6Flag = false
	MegaOhmFlag = false
	--byte 10
	B10Bit0Flag = false
	HzFlag = false
	FFlag = false
	CFlag = false
	B10Bit4Flag = false
	KiloFlag = false
	milliFlag = false
	B10Bit7Flag = false
	
	ACFlag = false
	
	HexValue = ByteArray[4]
	--print("***Value byte 4 " ..HexValue)
	BitValue = bit.band(HexValue, HoldBit)
	-- Check Hold Bit
	if BitValue >0 then
		HoldFlag = true
		--print("Hold on")
	end
	-- Check Buzzer Bit
	BitValue = bit.band(HexValue, BUZBit)
	if BitValue >0 then
		BUZFlag = true
		---print("Buzzer on")
	end
	-- Check Minus Bit
	BitValue = bit.band(HexValue, MinusBit)
	if BitValue >0 then
		MinusFlag = true
		--print("Minus on")
	end
	--Copy Ea 7 segment bits
	D1eaBit = bit.band(HexValue, DXeaBit)
	
	------------------------------------------------
	--Analys Byt 5
	HexValue = ByteArray[5]
	--print("***Value byte 5 " ..HexValue)
	-- copy dc 7 segement bits
	D1gcBit = bit.band(HexValue, DXgcBit)
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, DPBit)
	if BitValue >0 then
			DP2Flag = true
		--print("Decimal point 2 on")
	end
	D2eaBit = bit.band(HexValue, DXeaBit)
	------------------------------------------------
	--Analys Byt 6
	HexValue = ByteArray[6]
	--print("***Value byte 6 " ..HexValue)
	-- copy dc 7 segement bits
	D2gcBit = bit.band(HexValue, DXgcBit)
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, DPBit)
	if BitValue >0 then
			DP3Flag = true
		--print("Decimal point 3 on")
	end
	--Copy Ea 7 segment bits
	D3eaBit = bit.band(HexValue, DXeaBit)
	------------------------------------------------
	--Analys Byt 7
	HexValue = ByteArray[7]
	--print("***Value byte 7 " ..HexValue)
	-- copy dc 7 segement bits
	D3gcBit = bit.band(HexValue, DXgcBit)
	-- Check Decimal Point 2 Bit
	BitValue = bit.band(HexValue, DPBit)
	if BitValue >0 then
		DP4Flag = true
		--print("Decimal point 4 on")
	end
	--Copy Ea 7 segment bits
	D4eaBit = bit.band(HexValue, DXeaBit)
	------------------------------------------------
	--Analys Byt 8
	
	HexValue = ByteArray[8]
	--print("***Value byte 8 " ..HexValue)
	-- copy dc 7 segement bits
	D4gcBit = bit.band(HexValue, DXgcBit)
-- Check nano Bit
	BitValue = bit.band(HexValue, nanoBit)
	if BitValue >0 then
		nanoFlag = true
		--print("Nano on")
	end
	
	
	-- Check VoltBit Bit
	BitValue = bit.band(HexValue, VoltBit)
	if BitValue >0 then
		VoltFlag = true
		--print("Volt on")
		
		-- Check DCBit
		BitValue = bit.band(HexValue, DCBit)
		if BitValue >0 then
			DCFlag = true
			--print("DC on")
		else
			ACFlag = true
			--print("AC on")
		end
	end
	------------------------------------------------
	--Analys Byt 9

	HexValue = ByteArray[9]
	--print("***Value byte 9 " ..HexValue)
	
	-- Check FaradBit Bit
	BitValue = bit.band(HexValue, FaradBit)
	if BitValue >0 then
		FaradFlag = true
		--print("Farad on")
	end
	-- Check Diode Bit
	BitValue = bit.band(HexValue, DiodeBit)
	if BitValue >0 then
		DiodeFlag = true
		--print("Diode on")
	end
	-- Check AMPBit Bit
	BitValue = bit.band(HexValue, AmpBit)
	if BitValue >0 then
		AmpFlag = true
		--print("Amp on")
		-- Check DCBit
		BitValue = bit.band(HexValue, DCBit)
		if BitValue >0 then
			DCFlag = true
			--print("DC on")
		else
			ACFlag = true
			--print("AC on")
		end
	end
	-- Check microBit Bit
	BitValue = bit.band(HexValue, microBit)
	if BitValue >0 then
		microFlag = true
		--print("micro on")
	end
	
	-- Check Ohm bit
	BitValue = bit.band(HexValue, OhmBit)
	if BitValue >0 then
		OhmFlag = true
		--print("Ohm on")
	end
	
	-- Check B9Bit5 Bit
	BitValue = bit.band(HexValue, B9Bit5)
	if BitValue >0 then
		B9Bit5Flag = true
		print("9Bit5 on")
	end
	-- Check B9Bit6 Bit
	BitValue = bit.band(HexValue, B9Bit6)
	if BitValue >0 then
		B9Bit6Flag = true
		print("9Bit6 on")
	end
		-- Check MegaOhmBit Bit
	BitValue = bit.band(HexValue, MegaOhmBit)
	if BitValue >0 then
		MegaOhmFlag = true
		--print("MegaOhm on")
	end
	
	------------------------------------------------
	--Analys Byt 10
	
	HexValue = ByteArray[10]
	--print("***Value byte 10 " ..HexValue)	
	
	
	-- Check B10Bit0 Bit
	BitValue = bit.band(HexValue, B10Bit0)
	if BitValue >0 then
		B10Bit0Flag = true
		print("10Bit0 on")
	end
	-- Check Hz Bit
	BitValue = bit.band(HexValue, HzBit)
	if BitValue>0 then
		HzFlag = true
		--print("Hz on")
	end
	-- Check Fareignheit Bit
	BitValue = bit.band(HexValue, FBit)
	if BitValue>0 then
		FFlag = true
		--print("Farenheit on")
	end
	-- Check Celcius Bit
	BitValue = bit.band(HexValue, CBit)
	if BitValue>0 then
		CFlag = true
		--print("Celcius on")
	end
	-- Check B10Bit4 Bit
	BitValue = bit.band(HexValue, B10Bit4)
	if BitValue >0 then
		B10Bit4Flag = true
		print("10Bit4 on")
	end
	-- Check kilo Bit
	BitValue = bit.band(HexValue, KiloBit)
	if BitValue >0 then
		KiloFlag = true
		--print("Kilo on")
	end
	-- Check milli Bit
	BitValue = bit.band(HexValue, milliBit)
	if BitValue >0 then
		milliFlag = true
		--print("milli on")
	end

	-- Check B10Bit7 Bit
	BitValue = bit.band(HexValue, B10Bit7)
	if BitValue >0 then
		B10Bit7Flag = true
		print("10Bit7 on")
	end
	
	
end
-- Map bits to a number
MapDigits = function(endBits)
--[[
abecdfg
1111011   7B   = 0
0001010   0A   = 1
1011101   5D   = 2
1001111   4F   = 3
0101110   2E   = 4
1100111   67   = 5
1110111   77   = 6
1001010   4A   = 7
1111111   7F   = 8
1101111   6F   = 9
0110001   31   = L
]]--
	local Retchar = " "
	if  endBits == 0x7B then
		Retchar = "0"
	elseif endBits == 0x0A then
		Retchar = "1"
	elseif endBits == 0x5D then
		Retchar = "2"
	elseif endBits == 0x4F then
		Retchar = "3"
	elseif endBits == 0x2E then
		Retchar = "4"
	elseif endBits == 0x67 then
		Retchar = "5"
	elseif endBits == 0x77 then
		Retchar = "6"
	elseif endBits == 0x4A then
		Retchar = "7"
	elseif endBits == 0x7F then
		Retchar = "8"
	elseif endBits == 0x6F then
		Retchar = "9"
	elseif endBits == 0x31 then
		Retchar = "L"
	elseif endBits == 0x7E then
		Retchar = "A"
	elseif endBits == 0x13 then
		Retchar = "u"
	elseif endBits == 0x35 then
		Retchar = "t"
	elseif endBits == 0x17 then
		Retchar = "o"
	--else
		--print("Unknown "..string.format("%02x", endBits))
	end
	return Retchar
end
-- Used to process digits
Processdigits = function()
	
	local endBits = bit.rshift(D1eaBit,1)
	endBits = bit.bor(endBits,D1gcBit)
	Digit1 = MapDigits(endBits)
	--print("Digit 1 "..endBits)
	--print("Decode Digit 1 "..Digit1)
	--print("--------------")
	
	local endBits = bit.rshift(D2eaBit,1)
	endBits = bit.bor(endBits,D2gcBit)
	Digit2 = MapDigits(endBits)
	--print("Digit 2 "..endBits)
	--print("Decode Digit 2 "..Digit2)
	--print("--------------")
	
	local endBits = bit.rshift(D3eaBit,1)
	endBits = bit.bor(endBits,D3gcBit)
	Digit3 = MapDigits(endBits)
	--print("Digit 3 "..endBits)	
	--print("Decode Digit 3 "..Digit3)
	--print("--------------")
	local endBits = bit.rshift(D4eaBit,1)
	endBits = bit.bor(endBits,D4gcBit)
	Digit4 = MapDigits(endBits)
	--print("Digit 4 "..endBits)	
	--print("Decode Digit 4 "..Digit4)

end
-- Creates a string that is capable of displaying the whole display DMM 11 byte device
ProcessDisplayStr11 = function()
	DispString = ""
	if MinusFlag == true then
	DispString = "-"	
	end
	DispString = DispString..Digit1
	if DP2Flag == true then
	DispString = DispString.."."	
	end
	DispString = DispString..Digit2
	if DP3Flag == true then
	DispString = DispString.."."	
	end
	DispString = DispString..Digit3
	if DP4Flag == true then
	DispString = DispString.."."	
	end
	DispString = DispString..Digit4.." "
	-- checking Voltage
	if VoltFlag == true then
		if mVoltFlag == true then
			DispString = DispString.."m"
		end
		DispString = DispString.."V"
		if DCFlag == true then
			DispString = DispString.."dc "
		elseif ACFlag == true then
			DispString = DispString.."ac "
		end
		if DiodeFlag == true then
			DispString = DispString.."Diode "
		end
	end
	-- checking Amps
	if AmpFlag == true then
		if mAmpFlag == true then
			DispString = DispString.."m"
		elseif uAmpFlag == true then
			DispString = DispString.."u"
		end
		DispString = DispString.."A"
		if DCFlag == true then
			DispString = DispString.."dc "
		elseif ACFlag == true then
			DispString = DispString.."ac "
		end
	end
	-- checking Ohms
	if OhmFlag == true then
		if MegaOhmFlag == true then
			DispString = DispString.."M"
		elseif KiloOhmFlag == true then
			DispString = DispString.."k"
		end
		DispString = DispString.."Ohm "
		if BUZFlag == true then
		DispString = DispString.."Buzzer"
		end
	end
	-- checking Farad
	if FaradFlag == true then
		if uFFlag == true then
			DispString = DispString.."u"
		elseif mFFlag == true then
			DispString = DispString.."m"
		elseif nFFlag == true then
			DispString = DispString.."n"
		end
		DispString = DispString.."F"
	end
	-- checking Celcius
	if CFlag == true then
		DispString = DispString.."DegC"
	end
	-- checking Ferinhiet 
	if FFlag == true then
		DispString = DispString.."DegF"
	end
	-- checking Hertz
	if HzFlag == true then
		DispString = DispString.."Hz"
	end
	-- checking Percent
	if PercentFlag == true then
		DispString = DispString.."%"
	end
	-- checking Max
	if MaxFlag == true then
		DispString = DispString.."Max"
	end
	-- checking Min
	if MinFlag == true then
		DispString = DispString.."Min"
	end
	
	lprint("Device: "..DeviceRead..": "..DispString)
end
-- Creates a string that is capable of displaying the whole display for Tong 10 bit meter
ProcessDisplayStr10 = function()
	DispString = ""
	if MinusFlag == true then
	DispString = "-"	
	end
	DispString = DispString..Digit1
	if DP2Flag == true then
	DispString = DispString.."."	
	end
	DispString = DispString..Digit2
	if DP3Flag == true then
	DispString = DispString.."."	
	end
	DispString = DispString..Digit3
	if DP4Flag == true then
	DispString = DispString.."."	
	end
	DispString = DispString..Digit4.." "
	-- checking Voltage
	if VoltFlag == true then
		if milliFlag == true then
			DispString = DispString.."m"
		end
		DispString = DispString.."V"
		if DCFlag == true then
			DispString = DispString.."dc "
		elseif ACFlag == true then
			DispString = DispString.."ac "
		end
		if DiodeFlag == true then
			DispString = DispString.."Diode "
		end
		if BUZFlag == true then
			DispString = DispString.."Buzzer"
		end
	end
	-- checking Amps
	if AmpFlag == true then
		if milliFlag == true then
			DispString = DispString.."m"
		end
		DispString = DispString.."A"
		if DCFlag == true then
			DispString = DispString.."dc "
		elseif ACFlag == true then
			DispString = DispString.."ac "
		end
	end
	-- checking Ohms
	if OhmFlag == true then
		if MegaOhmFlag == true then
			DispString = DispString.."M"
		elseif KiloFlag == true then
			DispString = DispString.."k"
		end
		DispString = DispString.."Ohm "
		if BUZFlag == true then
			DispString = DispString.."Buzzer"
		end
	end
	-- checking Farad
	if FaradFlag == true then
		if nanoFlag == true then
			DispString = DispString.."n"
		end
		if microFlag == true then
			DispString = DispString.."u"
		end
		DispString = DispString.."F"
	end
	-- checking Celcius
	if CFlag == true then
		DispString = DispString.."DegC"
	end
	-- checking Ferinhiet 
	if FFlag == true then
		DispString = DispString.."DegF"
	end
	-- checking Hertz
	if HzFlag == true then
		DispString = DispString.."Hz"
	end
		
	lprint("Device: "..DeviceRead..": "..DispString)
end

lprint("Number of BT devices "..#arg)
while true do
	RunCommands()
	CheckResponse()
	DecodeBytes()
	if ReadSuccess == true then
		if DeviceType ~= 0 then
			if DeviceType == 10 then 
				ProcessElements10() 
				Processdigits()
				ProcessDisplayStr10()
			elseif DeviceType == 11 then
				ProcessElements11()
				Processdigits()
				ProcessDisplayStr11()
			end
			--TranslateDisplay()
			--PushtoMQTT()
		end
	end
	os.execute("sleep 5")
end
