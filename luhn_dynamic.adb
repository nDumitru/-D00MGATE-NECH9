-- =============================================================
-- D00MGATE-NECH9 -- Layer 1: Dynamic Luhn Token Body
-- Author: Dumitru Nechita
-- License: D00MGATE-NECH9 Proprietary v1.0
-- =============================================================
with Ada.Calendar;       use Ada.Calendar;
with Ada.Text_IO;        use Ada.Text_IO;
with GNAT.SHA256;
with Master_Key;         use Master_Key;

package body Luhn_Dynamic is

   -- ── Internal: Unix-like timestamp ────────────────────────────
   function Unix_Time return Long_Long_Integer is
      Epoch : constant Time := Time_Of (1970, 1, 1, 0.0);
   begin
      return Long_Long_Integer (Clock - Epoch);
   end Unix_Time;

   -- ── Current time window ───────────────────────────────────────
   function Current_Window return Long_Long_Integer is
   begin
      return Unix_Time / Window_Seconds;
   end Current_Window;

   -- ── Luhn algorithm ───────────────────────────────────────────
   function Luhn_Check (Number : String) return Boolean is
      Total  : Natural := 0;
      Double : Boolean := False;
      D      : Natural;
   begin
      -- Traverse right to left
      for I in reverse Number'Range loop
         if Number (I) in '0' .. '9' then
            D := Character'Pos (Number (I)) - Character'Pos ('0');
            if Double then
               D := D * 2;
               if D > 9 then D := D - 9; end if;
            end if;
            Total  := Total + D;
            Double := not Double;
         end if;
      end loop;
      return Total mod 10 = 0;
   end Luhn_Check;

   -- ── Compute Luhn check digit ─────────────────────────────────
   function Luhn_Digit (Partial : String) return Character is
      Total  : Natural := 0;
      Double : Boolean := True;  -- first from right is doubled (check pos)
      D      : Natural;
   begin
      for I in reverse Partial'Range loop
         if Partial (I) in '0' .. '9' then
            D := Character'Pos (Partial (I)) - Character'Pos ('0');
            if Double then
               D := D * 2;
               if D > 9 then D := D - 9; end if;
            end if;
            Total  := Total + D;
            Double := not Double;
         end if;
      end loop;
      D := (10 - (Total mod 10)) mod 10;
      return Character'Val (Character'Pos ('0') + D);
   end Luhn_Digit;

   -- ── Extract digits from SHA-256 hash ─────────────────────────
   function Extract_Digits (Hash : String; Count : Positive) return String is
      Result : String (1 .. Count) := (others => '0');
      Pos    : Positive := Result'First;
   begin
      for I in Hash'Range loop
         exit when Pos > Result'Last;
         if Hash (I) in '0' .. '9' then
            Result (Pos) := Hash (I);
            Pos := Pos + 1;
         end if;
      end loop;
      return Result;
   end Extract_Digits;

   -- ── Generate token for current window ────────────────────────
   function Generate_Token return Token_String is
      Window  : constant Long_Long_Integer := Current_Window;
      Win_Str : constant String := Long_Long_Integer'Image (Window);

      -- ┌────────────────────────────────────────────────────────┐
      -- │  TODO: DELTA NECHITA INTEGRATION                      │
      -- │  The seed below uses "DEMO_ONLY" prefix.              │
      -- │  Replace this prefix with your secret parameter       │
      -- │  combined with Master_Key_Value for production.       │
      -- │  Example structure (do NOT use as-is):               │
      -- │    Seed := "[YOUR_SECRET]" & Win_Str & "[YOUR_SALT]" │
      -- │  The exact combination is your Delta Nechita.        │
      -- └────────────────────────────────────────────────────────┘
      Seed    : constant String := "DEMO_ONLY_" & Win_Str;
      Hash    : constant String := GNAT.SHA256.Digest (Seed);
      D_Str   : constant String := Extract_Digits (Hash, Token_Length - 1);
      Check   : constant Character := Luhn_Digit (D_Str);
      Token   : Token_String;
   begin
      Token (1 .. Token_Length - 1) := D_Str;
      Token (Token_Length)          := Check;
      return Token;
   end Generate_Token;

   -- ── Validate a token ─────────────────────────────────────────
   function Validate_Token (Token : Token_String) return Boolean is
   begin
      return Validate_Full (Token) = Valid_Token;
   end Validate_Token;

   -- ── Full validation with detailed result ─────────────────────
   function Validate_Full (Token : Token_String) return Validation_Result is
      Current : constant Token_String := Generate_Token;
   begin
      -- Step 1: Luhn check (fast, cheap)
      if not Luhn_Check (Token) then
         return Invalid_Luhn;
      end if;

      -- Step 2: Window match
      if Token /= Current then
         -- ┌──────────────────────────────────────────────────────┐
         -- │  TODO: Add previous window tolerance if needed.     │
         -- │  Some systems allow current-1 window for clock skew.│
         -- │  Default: strict single window only.                │
         -- └──────────────────────────────────────────────────────┘
         return Wrong_Token;
      end if;

      return Valid_Token;
   end Validate_Full;

end Luhn_Dynamic;
