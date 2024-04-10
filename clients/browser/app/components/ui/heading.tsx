import { styled } from "@styled-system/jsx";

export const TopHeading = styled("h1", {
  base: {
    margin: 0,
    fontSize: 32,
    fontWeight: 500,
  },
});

export const SubHeading = styled("h2", {
  base: {
    margin: 0,
    fontSize: 16,
    color: "gray",
  },
});

export const Heading = {
  Top: TopHeading,
  Sub: SubHeading,
};
