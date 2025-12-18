import { createTheme, alpha, getContrastRatio, ThemeProvider } from '@mui/material/styles';
import Button from '@mui/material/Button';
import ButtonGroup from '@mui/material/ButtonGroup';
import { SwitcherProps } from '@/app/types/types';
const violetBase = '#d8b4fe';
const violetMain = alpha(violetBase, 0.7);

const theme = createTheme({
  palette: {
    secondary: {
      main: violetMain,
      light: alpha(violetBase, 0.5),
      dark: alpha(violetBase, 0.9),
      contrastText: getContrastRatio(violetMain, '#fff') > 4.5 ? '#fff' : '#111',
    },
  },
});



export default function PageSwitcher(props: SwitcherProps) {

    return (
        <ThemeProvider theme={theme}>
            <ButtonGroup variant="text" color="secondary" aria-label="Basic button group">
              <Button
                onClick={() => props.setShowHeroGraphic("default")}
                sx={{
                  bgcolor: "transparent",
                  color: props.showHeroGraphic === 'default' ? "inherit" : "#d8b4fe",
                  '&:hover': {
                    bgcolor: "secondary.light",
                  }
                }}>
                Overall Stats
              </Button>

              <Button
                onClick={() => props.setShowHeroGraphic("hero")}
                sx={{
                  bgcolor: "transparent",
                  color: props.showHeroGraphic === 'hero' ? "inherit" : "#d8b4fe",
                  '&:hover': {
                    bgcolor: "secondary.light",
                  }
                }}>
                Hero Stats
              </Button>

              <Button
                onClick={() => props.setShowHeroGraphic("map")}
                sx={{
                  bgcolor: "transparent",
                  color: props.showHeroGraphic === 'map' ? "inherit" : "#d8b4fe",
                  '&:hover': {
                    bgcolor: "secondary.light",
                  }
                }}>
                Map Stats
              </Button>

              <Button
                onClick={() => props.setShowHeroGraphic("charts")}
                sx={{
                  bgcolor: "transparent",
                  color: props.showHeroGraphic === 'charts' ? "inherit" : "#d8b4fe",
                  '&:hover': {
                    bgcolor: "secondary.light",
                  }
                }}>
                You Vs Top 1000
              </Button>

            </ButtonGroup>
          </ThemeProvider>
    )

}