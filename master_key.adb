-- =============================================================
-- D00MGATE-NECH9 -- Master Key Package Body
-- Author: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
with Ada.Text_IO;       use Ada.Text_IO;
with Ada.Strings.Fixed; use Ada.Strings.Fixed;
with Ada.Calendar;      use Ada.Calendar;
with GNAT.SHA512;

package body Master_Key is

   -- ============================================================
   --  ██████████████████████████████████████████████████████████
   --  ██                                                      ██
   --  ██  Master_Key_Value : constant String :=               ██
   --  ██     "MASTER_KEY_HERE";                               ██
   --  ██                                                      ██
   --  ██  Replace "MASTER_KEY_HERE" with your personal key.  ██
   --  ██  This is the ONLY location in the entire project.   ██
   --  ██  After replacing, recompile with:                   ██
   --  ██    gnatmake -P doomgate.gpr                         ██
   --  ██  NEVER commit the real value to Git.                ██
   --  ██  Add core/master_key.adb to .gitignore              ██
   --  ██                                                      ██
   --  ██████████████████████████████████████████████████████████
   -- ============================================================

   Master_Key_Value : constant String := "MASTER_KEY_HERE";  -- <- SET HERE

   -- Derived constants
   Key_Is_Set : constant Boolean :=
      Master_Key_Value /= "MASTER_KEY_HERE";

   Demo_Warning : constant String :=
      "WARNING: MASTER KEY NOT SET - DEMO MODE ONLY";

   Border : constant String (1 .. 54) := (others => '=');

   -- ── Internal SHA-512 hash of master key ──────────────────────
   function Key_Hash return String is
   begin
      if not Key_Is_Set then
         return "DEMO_HASH_NOT_REAL_00000000000000000000000000000000";
      end if;
      return GNAT.SHA512.Digest (Master_Key_Value);
   end Key_Hash;

   -- ── Simple hex XOR for demo signing (real impl: REDACTED) ────
   function Hex_Char (N : Natural) return Character is
      Hex : constant String := "0123456789abcdef";
   begin
      return Hex (Hex'First + (N mod 16));
   end Hex_Char;

   function Simple_Hash (Data : String) return Sig_String is
      Result : Sig_String := (others => '0');
      H      : String := Key_Hash;
      Val    : Natural;
   begin
      for I in Data'Range loop
         Val := (Character'Pos (Data (I)) +
                 Character'Pos (H ((I mod H'Length) + H'First))) mod 256;
         Result (((I - 1) * 2 mod Signature_Length * 2) + 1) :=
            Hex_Char (Val / 16);
         Result (((I - 1) * 2 mod Signature_Length * 2) + 2) :=
            Hex_Char (Val mod 16);
      end loop;
      return Result;
   end Simple_Hash;

   -- ── Public operations ─────────────────────────────────────────

   function Is_Ready return Boolean is
   begin
      return Key_Is_Set;
   end Is_Ready;

   function Get_Status return Key_Status is
   begin
      if Key_Is_Set then
         return Key_Ready;
      else
         return Key_Demo_Mode;
      end if;
   end Get_Status;

   procedure Warn (Function_Name : String := "") is
   begin
      if not Key_Is_Set then
         Put_Line (Border);
         Put_Line ("  " & Demo_Warning);
         if Function_Name /= "" then
            Put_Line ("  '" & Function_Name & "' needs real Master Key.");
         end if;
         Put_Line ("  Edit: core/master_key.adb -> Master_Key_Value");
         Put_Line (Border);
      end if;
   end Warn;

   function Require (Function_Name : String) return Boolean is
   begin
      if not Key_Is_Set then
         Warn (Function_Name);
         return False;
      end if;
      return True;
   end Require;

   function Sign (Data : String) return Sig_String is
   begin
      if not Key_Is_Set then
         return (others => '0');  -- UNSIGNED_DEMO
      end if;
      return Simple_Hash (Key_Hash & ":" & Data);
      -- TODO: Replace Simple_Hash with HMAC-SHA256 in production
      -- Real implementation uses Ada.Digest or liboqs binding
   end Sign;

   function Verify (Data : String; Sig : Sig_String) return Boolean is
   begin
      if not Key_Is_Set then
         return False;
      end if;
      return Sign (Data) = Sig;
   end Verify;

   -- ── OMEGA-49 sequence generation ─────────────────────────────
   function Get_Omega_Sequence (Epoch : Long_Long_Integer)
      return Omega_Sequence
   is
      Seed   : constant String := Master_Key_Value & Long_Long_Integer'Image (Epoch);
      Digest : constant String := GNAT.SHA512.Digest (Seed);
      Result : Omega_Sequence;
      Domain : constant array (1 .. 14) of Valid_Domain :=
         (-7, -6, -5, -4, -3, -2, -1, 1, 2, 3, 4, 5, 6, 7);
      Idx    : Positive;
      Byte   : Natural;
   begin
      for I in Result'Range loop
         Byte := Character'Pos (Digest (Digest'First + (I - 1) mod Digest'Length));
         Idx  := (Byte mod 14) + 1;
         Result (I) := Domain (Idx);
      end loop;
      return Result;
   end Get_Omega_Sequence;

end Master_Key;
