import * as AvatarPrimitive from "@radix-ui/react-avatar";
import { styled } from "@styled-system/jsx";
import { DetailedHTMLProps, HTMLAttributes } from "react";

export const AvatarRoot = styled(AvatarPrimitive.Root, {
  base: {
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    width: 10,
    height: 10,
    borderRadius: "50%",
    backgroundColor: "gainsboro",
    color: "black",
    flexShrink: 0,
  },
});

export const AvatarImage = styled(AvatarPrimitive.Image, {
  base: {
    width: "100%",
    height: "100%",
    borderRadius: "inherit",
  },
});

export const AvatarFallback = styled(AvatarPrimitive.Fallback, {
  base: {
    width: "100%",
    height: "100%",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    borderRadius: "inherit",
    userSelect: "none",
    color: "white",
    fontSize: 14,
  },
});

const AvatarGroupPrimitive: React.FC<
  {
    children?: React.ReactNode;
  } & DetailedHTMLProps<HTMLAttributes<HTMLDivElement>, HTMLDivElement>
> = ({ children, ...props }) => {
  return <div {...props}>{children}</div>;
};

export const AvatarGroup = styled(AvatarGroupPrimitive, {
  base: {
    display: "flex",
    paddingLeft: 4,
    "& > span": {
      marginLeft: -2,
      transition: "transform 0.2s",
    },
  }
});

export const Avatar = Object.assign(AvatarRoot, {
  Root: AvatarRoot,
  Image: AvatarImage,
  Fallback: AvatarFallback,
  Group: AvatarGroup,
});
