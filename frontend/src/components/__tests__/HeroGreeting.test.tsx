import React from 'react';
import { render, screen } from '@testing-library/react';
import HeroGreeting from '../HeroGreeting';

describe('HeroGreeting Component', () => {
    it('renders greeting headings', () => {
        render(<HeroGreeting />);
        expect(screen.getByRole('heading', { level: 1 })).toHaveTextContent('Good Morning, [User].');
        expect(screen.getByText('Ask a Tax Question.')).toBeInTheDocument();
    });
});
