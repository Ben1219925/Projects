library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity tristate is
  Port (read, dataIn : in std_logic;
        DataBUS : inout std_logic;  -- needs to be initialized in TB as High Impedence
        IntBus : out std_logic);
end tristate;

architecture Behavioral of tristate is

begin

DataBUS <= dataIn when read = '0' else 'Z';
IntBus <= DataBUS;

end Behavioral;