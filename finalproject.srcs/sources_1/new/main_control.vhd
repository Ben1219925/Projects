library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity main_control is
    Port(clk, rst, cmd_received, uart_busy, i2c_busy, spi_busy, spi_done: in std_logic;
         i2c_led_in: in std_logic_vector(5 downto 0);
         spi_led_in: in std_logic_vector(5 downto 0);
         i2c_cs_led: in std_logic_vector(3 downto 0);
         spi_cs_led: in std_logic_vector(1 downto 0);  
         command: in std_logic_vector(7 downto 0);
         led_out: out std_logic_vector(5 downto 0);
         i2c_start, i2c_switch, spi_start, spi_switch: out std_logic);
end main_control;

architecture Behavioral of main_control is
type state_type is (idle, exec);
signal cs: state_type:= idle;
signal done_s, store_s, first_cmd: std_logic;
begin
process(clk,rst)
begin
    if rst = '1' then
        led_out <= (others => '0');
        i2c_switch <= '0';
        spi_start <= '0';
        spi_switch <= '0';
        i2c_start <= '0';
        store_s <= '0';
        done_s <= '0';
        first_cmd <= '1';
    elsif rising_edge(clk) then
        case cs is
--------------------IDLE-------------------------------------------------------------------------
            when idle =>
                if cmd_received = '1' then
                    cs <= exec;
                    spi_start <= '1';
                    if first_cmd = '1' then
                        i2c_start <= '1';
                        first_cmd <= '0';
                    else
                        i2c_start <= '0';
                    end if;
                else
                    cs <= idle;
                end if;
-------------------EXEC------------------------------------------------------------------
            when exec =>                 
                if command(0) = '0' then
                    i2c_switch <= '0';
                    spi_switch <= '0';
                else
                    i2c_switch <= '1';
                    spi_switch <= '1';
                end if;
                --ADC lights
                if command(1) = '1' then
                    led_out <= i2c_led_in;
                --DAC lights
                elsif command(2) = '1' then
                    led_out <= spi_led_in;
                --state lights
                elsif command(3) = '1' then
                    led_out <= i2c_cs_led & spi_cs_led;
                --stop signal generation
                else
                    led_out <= i2c_cs_led & spi_cs_led;
                    spi_start <= '0';
                    i2c_start <= '0';
                    i2c_switch <= '0';
                    spi_switch <= '0';
                    cs <= idle;
                end if;
                
                if spi_done = '1' then
                    i2c_start <= '1';
                else
                    i2c_start <= '0';
                end if;
                
        end case;                
    end if;  
           
end process;

end Behavioral;
