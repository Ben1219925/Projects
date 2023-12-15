library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity controller1 is
Port (clk, rst, start, dataIn, switch: in std_logic;
      read, busy, addr, i2c_clk: out std_logic;
      cs_led: out std_logic_vector(3 downto 0);
      dataOut: out std_logic_vector(17 downto 0);
      i2done : out std_logic); 
end controller1;

architecture Behavioral of controller1 is
type state_type is (waiting, configure, Conack, idle, transmit1, transmit2, ack, receive, masterack, stop);
signal cs: state_type:= waiting;
signal count_s: integer range 0 to 1000 := 0; --100KHZ CLOCK SPEED
signal bit_num : integer range 0 to 8 := 8;
signal data_bit: integer range 0 to 18:= 18;
signal done, acked_s: std_logic := '0';
signal read_s, busy_s, addr_s, i2c_clk_s, count_en: std_logic;
signal dataOut_s: std_logic_vector(17 downto 0);
constant count: integer := 1000;
constant config: std_logic_vector(17 downto 0) := "010100000000100000"; --CONFIGURING BITS
constant address: std_logic_vector(7 downto 0) := "01010001"; --ADDRESS BITS
signal i2done_s : std_logic; 

begin
process(clk,rst)
begin
    if rst = '1' then
        cs <= waiting;
        i2c_clk_s <= '1';
        read_s <= '0';
        bit_num <= 8;
        data_bit <= 18;
        addr_s <= '1';    
        acked_s <= '0';
        dataOut_s <= (others => '0');
        busy_s <= '0';
        count_en <= '0';
        i2done_s <= '0';
    elsif rising_edge(clk) then
        case cs is
-------------------------WAITING----------------------------------------
            when waiting =>
                cs_led <= "0000";
                i2c_clk_s <= '1';
                read_s <= '0';
                busy_s <= '0';
                addr_s <= '1';
                count_en <= '0';
                if start = '1' then
                    count_en <= '1';
                    addr_s <= '0';
                    cs <= configure;
                    busy_s <= '1';
                else
                    cs <= waiting;
                end if; 
-------------------------CONFIGURE----------------------------------------
            when configure =>
                cs_led <= "0001";
                if done = '1' then
                    i2c_clk_s <= not i2c_clk_s;
                    if data_bit = 10 and i2c_clk_s = '1'  then
                        cs <= conack;
                        data_bit <= data_bit -1;
                        read_s <= '1';      
                    elsif data_bit = 1 and i2c_clk_s = '1' then
                        cs <= conack;
                        data_bit <= data_bit -1;
                        read_s <= '1';
                    elsif i2c_clk_s = '1' then
                        addr_s <= config(data_bit -1);
                        data_bit <= data_bit -1;
                    else
                        cs <= configure;
                    end if;
                end if; 
-------------------------CONACK----------------------------------------
            when conack =>
                cs_led <= "0001";
                if done = '1' then
                    i2c_clk_s <= not i2c_clk_s; 
                    if dataIn = '0' and data_bit = 9 and i2c_clk_s = '0' then
                        cs <= conack;
                        --data_bit <= data_bit -1; 
                    elsif data_bit = 9 and i2c_clk_s = '1' then
                        cs <= configure; 
                        data_bit <= data_bit -1; 
                        read_s <= '0'; 
                   elsif datain = '0' and data_bit = 0 and i2c_clk_s = '0' then
                        data_bit <= 18;
                   elsif data_bit = 18 and i2c_clk_s = '1' then
                        cs <= stop;
                        addr_s <= '0';
                        read_s <= '0';
                   elsif i2c_clk_s = '0' then
                        cs <= waiting;
                        data_bit <= 18;
                   else
                        cs <= conack; 
                   end if; 
               else
                    cs <= conack; 
               end if; 
-------------------------IDLE----------------------------------------
            when idle =>
                cs_led <= "0010";
                i2c_clk_s <= '1';
                read_s <= '0';
                busy_s <= '0';
                acked_s <= '0';
                addr_s <= '1';
                i2done_s <= '0'; 
                if start = '1' then
                    if done = '1' then
                        cs <= transmit2;
                        busy_s <= '1';
                        addr_s <= address(7);
                    else
                        cs <= idle;
                    end if;
                else
                    cs <= idle;
                end if; 
-------------------------TRANSMIT1----------------------------------------
            when transmit1 =>
                cs_led <= "0100";
                if done = '1' then
                    cs <= transmit2;
                    i2c_clk_s <= '1';
                else
                    cs <= transmit1;
                end if;    
-------------------------TRANSMIT2----------------------------------------
            when transmit2 =>
                cs_led <= "0100";
                if bit_num = 0 and done = '1' then
                    cs <= ack;
                    bit_num <= 8;
                    read_s <= '1';
                    i2c_clk_s <= '0';
                elsif done = '1' then
                    cs <= transmit1;
                    addr_s <= address(bit_num-1);
                    bit_num <= bit_num - 1;
                    i2c_clk_s <= '0';
                else
                    cs <= transmit2;
                end if;
-------------------------ACK----------------------------------------
            when ack =>   
                cs_led <= "0100";
                if done = '1' then
                    i2c_clk_s <= not i2c_clk_s;
                    if i2c_clk_s = '0' and dataIn = '0' then
                        dataOut_s(data_bit-1) <= dataIn;
                        data_bit <= data_bit -1;                        
                    elsif data_bit = 17 then
                        cs <= receive;
                    elsif i2c_clk_s = '1' then
                        cs <= idle;
                    else
                        cs <= ack;
                    end if;
                else
                    cs <= ack;
                end if;
-------------------------RECIEVE----------------------------------------
            when receive =>
                i2done_s <= '0'; 
                cs_led <= "1000";
                read_s <= '1';
                if done = '1' then
                    i2c_clk_s <= not i2c_clk_s;
                    if data_bit = 9 and acked_s = '0' and i2c_clk_s = '1'  then
                        cs <= masterack;
                        read_s <= '0';
                        addr_s <= '0';      
                    elsif data_bit = 0 and i2c_clk_s = '1' and switch = '1' then --CONTINUOUS READ
                        cs <= masterack;
                        read_s <= '0';
                        addr_s <= '0';
                    elsif data_bit = 0 and i2c_clk_s = '1' and switch = '0' then
                        cs <= masterack;
                        read_s <= '0';
                        addr_s <= '1';
                    elsif i2c_clk_s = '0' then
                        dataOut_s(data_bit-1) <= dataIn;
                        data_bit <= data_bit -1;
                    else
                        cs <= receive;
                    end if;
                else
                    i2c_clk_s <= i2c_clk_s;
                    cs <= receive;
                    data_bit <= data_bit;
                end if;
-------------------------MASTERACK----------------------------------------
            when masterack =>
                cs_led <= "1000";
                if done = '1' then
                    i2c_clk_s <= not i2c_clk_s;
                    if i2c_clk_s = '0' and data_bit = 9 then
                        dataOut_s(data_bit-1) <= dataIn;
                        data_bit <= data_bit - 1;
                    elsif i2c_clk_s = '1' and data_bit = 8 then
                        cs <= receive;
                        acked_s <= '1'; 
                    elsif i2c_clk_s = '0' and data_bit = 0 then
                        cs <= masterack;
                    elsif i2c_clk_s = '1' and data_bit = 0 and switch = '1' then --CONTINUOUS READ
                        data_bit <= 17;
                        acked_s <= '0';
                        read_s <= '1';
                        cs <= receive;
                        i2done_s <= '1';
                    elsif i2c_clk_s = '1' and data_bit = 0 and switch = '0' then
                        data_bit <= 18;
                        addr_s <= '0';
                        i2done_s <= '1'; 
                        cs <= stop;
                    else
                        cs <= masterack;
                    end if;
                else
                    i2c_clk_s <= i2c_clk_s;
                    cs <= masterack;
                end if;           
-------------------------STOP----------------------------------------
            when stop =>
                cs_led <= "1000";
                i2done_s <= '0'; 
                if done = '1' then
                    i2c_clk_s <= '1';
                    if i2c_clk_s = '1' then
                        addr_s <= '1';
                        cs <= idle;
                    else
                        cs <= stop;
                    end if;
                else
                    cs <= stop;
                end if;
        end case;
    end if;
end process;
    i2c_clk <= i2c_clk_s;
    read <= read_s;
    busy <= busy_s;
    addr <= addr_s;
    dataOut <= dataOut_s;
    i2done <= i2done_s; 
    
    
-------------------------COUNTER----------------------------------------
process(clk,rst)
    begin
        if rst = '1' then
            count_s <= 0;
        elsif falling_edge(clk) then
            done <= '0';
            if count_en = '1' then
                if count_s = count then
                    done <= '1';
                    count_s <= 0;
                else
                    count_s <= count_s + 1;
                end if;
            else
                count_s <= 0;
            end if;            
        end if;
end process;

end Behavioral;
