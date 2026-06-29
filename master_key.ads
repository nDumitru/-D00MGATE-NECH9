-- =============================================================
-- D00MGATE-NECH9 -- Master Key Package
-- Author: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
--
-- ┌─────────────────────────────────────────────────────────┐
-- │  MASTER KEY CONFIGURATION                               │
-- │  Search: MASTER_KEY_HERE  (1 location in master_key.adb)│
-- │  Replace with your personal key before compilation.     │
-- │  NEVER commit the real value to Git.                    │
-- └─────────────────────────────────────────────────────────┘
--
package Master_Key is

   -- Key length constants
   Key_Length      : constant := 64;   -- bytes
   Signature_Length: constant := 32;   -- bytes
   Hash_Length     : constant := 64;   -- bytes (SHA-512 output)

   -- Key status
   type Key_Status is (Key_Ready, Key_Demo_Mode);

   -- Subtypes
   subtype Key_String     is String (1 .. Key_Length * 2);  -- hex
   subtype Sig_String     is String (1 .. Signature_Length * 2);
   subtype Hash_String    is String (1 .. Hash_Length * 2);
   subtype Raw_Key        is String (1 .. 256);  -- raw input

   -- Main operations
   function  Is_Ready       return Boolean;
   function  Get_Status     return Key_Status;
   function  Sign           (Data : String) return Sig_String;
   function  Verify         (Data : String; Sig : Sig_String) return Boolean;
   procedure Warn           (Function_Name : String := "");
   function  Require        (Function_Name : String) return Boolean;

   -- Domain constants (OMEGA-49)
   type Domain_Value is range -7 .. 7;
   subtype Valid_Domain is Domain_Value
      with Static_Predicate => Valid_Domain /= 0;

   -- OMEGA-49 sequence
   type Omega_Sequence is array (1 .. 7) of Valid_Domain;
   function Get_Omega_Sequence (Epoch : Long_Long_Integer)
      return Omega_Sequence;

end Master_Key;
