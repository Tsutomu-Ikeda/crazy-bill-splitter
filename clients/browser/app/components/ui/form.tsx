import * as FormPrimitive from "@radix-ui/react-form";
import { styled } from "@styled-system/jsx";

export const FormRoot = styled(FormPrimitive.Root, {
  base: {
    display: "grid",
    gap: 2,
  },
});

export const FormLabel = styled(FormPrimitive.Label, {
  base: {
    fontSize: 14,
    color: "gray",
  },
});

export const FormItem = styled("div", {
  base: {
    display: "grid",
    gap: 5,
  },
});

export const FormButton = styled(FormPrimitive.Submit, {
  base: {
    fontSize: 14,
    padding: "10px 15px",
    border: "1px solid gainsboro",
    borderRadius: 5,
    backgroundColor: "white",
    cursor: "pointer",
  },
});

export const FormControl = styled(FormPrimitive.Control, {
  base: {
    fontSize: 14,
    padding: "10px 15px",
    border: "1px solid gainsboro",
    borderRadius: 5,
  },
});

export const FormField = styled(FormPrimitive.Field, {
  base: {
    display: "grid",
    gap: 5,
  },
});

export const Form = Object.assign(FormRoot, {
  Root: FormRoot,
  Item: FormItem,
  Label: FormLabel,
  Button: FormButton,
  Control: FormControl,
  Field: FormField,
});
